import os
import logging
import chess
import chess.engine
from flask import Flask, render_template, request, jsonify

# Set up logging for debugging and error tracking
logging.basicConfig(level=logging.INFO)

# ---------------------------
# Chess Game Logic 
# ---------------------------
class ChessGame:
    def __init__(self, openings_file="openings.txt"):
        self.board = chess.Board()
        self.moves_log = []       # Stores moves in SAN
        self.redo_stack = []      # For undo/redo functionality
        self.game_results = {"win": 0, "loss": 0, "draw": 0}
        self.openings_dataset = self.load_openings(openings_file) 

    def load_openings(self, filename):
        openings = []
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ":" in line:
                        moves_part, name = line.split(":", 1)
                        moves_seq = moves_part.strip().split()
                        name = name.strip()
                        openings.append((moves_seq, name))
        except Exception as e:
            logging.error("Error loading openings: %s", e)
        return openings

    def board_to_dict(self):
        piece_unicode = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        board_dict = {}
        for rank in range(8, 0, -1):
            for file in "abcdefgh":
                square_name = file + str(rank)
                square_index = chess.parse_square(square_name)
                piece = self.board.piece_at(square_index)
                board_dict[square_name] = piece_unicode[piece.symbol()] if piece else ''
        return board_dict

    def get_opening_name(self):
        best_match = ""
        best_length = 0
        for seq, name in self.openings_dataset:
            if len(seq) <= len(self.moves_log) and self.moves_log[:len(seq)] == seq:
                if len(seq) > best_length:
                    best_length = len(seq)
                    best_match = name
        return best_match

    def get_game_stats(self):
        initial_count = 16  # each side starts with 16 pieces
        white_count = 0
        black_count = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    white_count += 1
                else:
                    black_count += 1
        captured_white = initial_count - white_count
        captured_black = initial_count - black_count

        piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}
        white_material = 0
        black_material = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                val = piece_values[piece.symbol().lower()]
                if piece.color == chess.WHITE:
                    white_material += val
                else:
                    black_material += val
        material_diff = white_material - black_material
        return {
            "moves_made": len(self.moves_log),
            "white_captured": captured_white,
            "black_captured": captured_black,
            "white_material": white_material,
            "black_material": black_material,
            "material_diff": material_diff
        }

    def make_move(self, move_str, promotion=None):
        """
        Processes a move in UCI format. For a pawn move reaching the last rank, if the move string
        is only 4 characters long (i.e. no promotion piece specified), it checks for a promotion parameter.
        """
        try:
            move = chess.Move.from_uci(move_str)
        except Exception:
            raise ValueError("Invalid move format")
        
        piece = self.board.piece_at(move.from_square)
        # Check for pawn promotion: pawn moving to the first or last rank
        if piece and piece.piece_type == chess.PAWN and chess.square_rank(move.to_square) in [0, 7]:
            if len(move_str) == 4:
                if promotion is None:
                    raise ValueError("Promotion piece required")
                else:
                    move_str = move_str + promotion.lower()
                    try:
                        move = chess.Move.from_uci(move_str)
                    except Exception:
                        raise ValueError("Invalid promotion move format")
        
        if move in self.board.legal_moves:
            self.redo_stack = []
            san = self.board.san(move)
            self.board.push(move)
            self.moves_log.append(san)
            return san
        else:
            raise ValueError("Illegal move")

    def undo_move(self):
        if len(self.board.move_stack) > 0:
            last_move = self.board.pop()
            if self.moves_log:
                self.moves_log.pop()
            self.redo_stack.append(last_move)
            return True
        return False

    def redo_move(self):
        if self.redo_stack:
            move = self.redo_stack.pop()
            self.board.push(move)
            san = self.board.san(move)
            self.moves_log.append(san)
            return True
        return False

    def reset(self):
        self.board.reset()
        self.moves_log = []
        self.redo_stack = []

# ---------------------------
# Chess Engine Analysis 
# ---------------------------
class ChessEngine:
    def __init__(self, engine_path):
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        except FileNotFoundError as e:
            logging.error("Stockfish binary not found at %s", engine_path)
            raise FileNotFoundError(
                f"Stockfish binary not found at {engine_path}. Please install Stockfish and/or update STOCKFISH_PATH environment variable."
            ) from e

    def analyse_position(self, board, time_limit=0.1, multipv=2):
        try:
            result = self.engine.analyse(board, chess.engine.Limit(time=time_limit), multipv=multipv)
            best_moves = []
            for analysis in result:
                move = analysis['pv'][0]
                score_obj = analysis['score'].relative
                if score_obj.is_mate():
                    score_value = 10000 if score_obj.mate() > 0 else -10000
                else:
                    score_value = score_obj.score()
                best_moves.append({
                    'uci': move.uci(),
                    'from': chess.square_name(move.from_square),
                    'to': chess.square_name(move.to_square),
                    'score': score_value
                })
            return best_moves
        except Exception as e:
            logging.error("Engine analysis failed: %s", e)
            raise e

    def close(self):
        self.engine.quit()

# ---------------------------
# Flask App and Routes
# ---------------------------
app = Flask(__name__)

# Read engine path from environment variables (or use default)
ENGINE_PATH = os.environ.get("STOCKFISH_PATH", "/opt/homebrew/bin/stockfish")
game = ChessGame()
engine = ChessEngine(ENGINE_PATH)
engine_mode_enabled = False  # Global toggle for engine analysis

@app.route('/')
def index():
    board_state = game.board_to_dict()
    return render_template('index.html', board=board_state)

@app.route('/toggle_engine', methods=['POST'])
def toggle_engine():
    global engine_mode_enabled
    data = request.get_json()
    engine_mode_enabled = data.get('enabled', False)
    return jsonify({'engine_mode': engine_mode_enabled})

@app.route('/get_best_moves', methods=['GET'])
def get_best_moves():
    if not engine_mode_enabled:
        return jsonify({'best_moves': []})
    try:
        best_moves = engine.analyse_position(game.board)
        return jsonify({'best_moves': best_moves})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_legal_moves', methods=['POST'])
def get_legal_moves():
    data = request.get_json()
    square = data.get('square')
    square_index = chess.parse_square(square)
    piece = game.board.piece_at(square_index)
    if not piece:
        return jsonify({'legal_moves': []})
    moves = []
    for move in game.board.legal_moves:
        if chess.square_name(move.from_square) == square:
            moves.append(chess.square_name(move.to_square))
    return jsonify({'legal_moves': moves})

@app.route('/make_move', methods=['POST'])
def make_move_route():
    data = request.get_json()
    move_str = data.get('move')
    promotion = data.get('promotion')  # Optional: one of 'q', 'r', 'b', 'n'
    try:
        game.make_move(move_str, promotion)
        board_state = game.board_to_dict()
        opening = game.get_opening_name()
        stats = game.get_game_stats()
        game_over = game.board.is_game_over()
        outcome = ""
        if game_over:
            result = game.board.result()  # "1-0", "0-1", "1/2-1/2"
            if result == "1-0":
                game.game_results["win"] += 1
                outcome = "Player wins!"
            elif result == "0-1":
                game.game_results["loss"] += 1
                outcome = "Player loses!"
            else:
                game.game_results["draw"] += 1
                outcome = "Draw!"
        return jsonify({
            'success': True,
            'board': board_state,
            'moves': game.moves_log,
            'opening': opening,
            'stats': stats,
            'game_over': game_over,
            'outcome': outcome,
            'game_results': game.game_results
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/undo', methods=['POST'])
def undo():
    try:
        if game.undo_move():
            board_state = game.board_to_dict()
            stats = game.get_game_stats()
            return jsonify({'success': True, 'board': board_state, 'moves': game.moves_log, 'stats': stats})
        else:
            return jsonify({'error': 'No moves to undo'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/redo', methods=['POST'])
def redo():
    try:
        if game.redo_move():
            board_state = game.board_to_dict()
            stats = game.get_game_stats()
            return jsonify({'success': True, 'board': board_state, 'moves': game.moves_log, 'stats': stats})
        else:
            return jsonify({'error': 'No moves to redo'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    game.reset()
    board_state = game.board_to_dict()
    stats = game.get_game_stats()
    return jsonify({
        'success': True,
        'board': board_state,
        'moves': game.moves_log,
        'opening': "",
        'stats': stats,
        'game_over': False,
        'outcome': "",
        'game_results': game.game_results
    })

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        engine.close()
