import pyxel
import random

class APP:
    def __init__(self):
        pyxel.init(70, 100, title="SAKURA CATCHER")
        pyxel.load('pyxel.pyxres')

        self.avatar_x = pyxel.width // 2
        self.score = 0
        self.petals = []
        self.shrimps = []
        self.text_objects = []  # Text objects list

        self.frame_count = 0  # アニメーション用フレームカウンター
        self.current_avatar_image = 0  # 現在のアバター画像のインデックス

        self.game_stage = 1  # ゲームのステージを管理
        self.game_started = False
        self.countdown = 4  # カウントダウンの初期値
        self.game_time_limit = 45  # ステージ1のゲームプレイ時間（秒）
        self.start_time = pyxel.frame_count
        self.game_end_time = None  # ゲーム終了時刻
        self.remaining_time = 0  # 残り時間の初期値
        self.game_ended = False  # ゲーム終了フラグ

        self.show_message_screen = False  # 特別な画面表示のフラグ

        # 定義した4つの桜エビのグラフィックの座標
        self.shrimp_graphics = [
            (0, 16, 6, 6, 0),  # 1番目のグラフィック
            (8, 16, 6, 6, 0),  # 2番目のグラフィック
            (0, 24, 6, 6, 0),  # 3番目のグラフィック
            (8, 24, 6, 6, 0)   # 4番目のグラフィック
        ]

        # 定義した4つの文字オブジェクトのグラフィックの座標
        self.text_graphics = [
            (0, 48, 16, 8),  # 1番目のグラフィック
            (0, 56, 16, 8),  # 2番目のグラフィック
            (24,48, 16, 8), # 3番目のグラフィック
            (24, 56, 16, 8)  # 4番目のグラフィック
        ]

        pyxel.run(self.update, self.draw)

    def reset_game(self, next_stage=False):
        self.avatar_x = pyxel.width // 2
        self.score = 0
        self.petals = []
        self.shrimps = []
        self.text_objects = []  # Reset text objects list

        self.frame_count = 0
        self.current_avatar_image = 0
        self.game_started = False
        self.countdown = 4
        self.start_time = pyxel.frame_count
        self.game_end_time = None
        self.remaining_time = 0
        self.game_ended = False

        if next_stage:
            self.game_stage = 2
            self.game_time_limit = 60  # Set time limit for Stage 2
        else:
            self.game_stage = 1  # 完全に初期状態にリセット

    def add_petal(self):
        self.petals.append({
            "x": random.randint(0, pyxel.width - 12),
            "y": 0,
            "speed_x": random.uniform(-0.5, 0.5),
            "speed_y": random.uniform(0.5, 1.5)
        })

    def add_shrimp(self):
        # ランダムにグラフィックを選択
        graphic = random.choice(self.shrimp_graphics)
        self.shrimps.append({
            "x": random.randint(0, pyxel.width - graphic[4]),
            "y": 0,
            "speed_x": random.uniform(-0.3, 0.3),
            "speed_y": random.uniform(0.7, 1.2),
            "graphic": graphic  # ここで選択したグラフィックを保存
        })

    def add_text_object(self):
        # ランダムにグラフィックを選択
        graphic = random.choice(self.text_graphics)
        self.text_objects.append({
            "x": random.randint(0, pyxel.width - graphic[2]),
            "y": 0,
            "speed_y": random.uniform(1.0, 2.0),
            "graphic": graphic  # ここで選択したグラフィックを保存
        })

    def update(self):
        current_frame = pyxel.frame_count

        if self.show_message_screen:
            if pyxel.btn(pyxel.KEY_SPACE):
                self.show_message_screen = False
                self.reset_game(next_stage=True)
            return

        # アバターの位置をマウスで制御
        self.avatar_x = max(0, min(pyxel.mouse_x, pyxel.width - 12))

        # アニメーションの更新処理
        if current_frame % 15 == 0:  # 15フレームごとに切り替え
            self.current_avatar_image = 1 - self.current_avatar_image  # 0と1を交互に切り替え

        if not self.game_started:
            # カウントダウン処理
            if (current_frame - self.start_time) % 30 == 0 and self.countdown > 0:  # 1秒ごとにカウントダウン
                self.countdown -= 1

            if self.countdown == 0:
                # ゲームスタート
                self.game_started = True
                self.game_end_time = current_frame + self.game_time_limit * 30  # ステージに応じた45秒または60秒後のフレームを設定
                # 初期状態でオブジェクトを設定
                for _ in range(5):
                    self.add_petal()
                if self.game_stage == 1:
                    self.add_shrimp()
                else:
                    # ステージ2では文字オブジェクトも生成
                    for _ in range(3):
                        self.add_text_object()

        if self.game_started and not self.game_ended:
            # ゲームがスタートした後の処理
            self.frame_count += 1

            # 花弁の更新
            for petal in self.petals:
                petal["x"] += petal["speed_x"]
                petal["y"] += petal["speed_y"]

                if petal["y"] > pyxel.height:
                    self.petals.remove(petal)
                    self.add_petal()

                if abs(self.avatar_x - petal["x"]) < 10 and abs(70 - petal["y"]) < 10:
                    if self.game_stage == 1:
                        self.score -= 183  # 得点を変更
                    elif self.game_stage == 2:
                        self.score += 200  # ステージ2では得点を追加
                    self.petals.remove(petal)
                    self.add_petal()

            # 桜エビの更新（ステージ1のみ）
            if self.game_stage == 1:
                for shrimp in self.shrimps:
                    shrimp["x"] += shrimp["speed_x"]
                    shrimp["y"] += shrimp["speed_y"]

                    if shrimp["y"] > pyxel.height:
                        self.shrimps.remove(shrimp)
                        self.add_shrimp()

                    if abs(self.avatar_x - shrimp["x"]) < 10 and abs(70 - shrimp["y"]) < 10:
                        self.score += 20  # 得点を変更
                        self.shrimps.remove(shrimp)
                        self.add_shrimp()

                # 桜エビを3分の1の確率で追加
                if random.randint(1, 100) <= 3:  # 3%の確率で追加
                    self.add_shrimp()

            # 文字オブジェクトの更新（ステージ2のみ）
            if self.game_stage == 2:
                for text_obj in self.text_objects:
                    text_obj["y"] += text_obj["speed_y"]

                    if text_obj["y"] > pyxel.height:
                        self.text_objects.remove(text_obj)
                        self.add_text_object()

                    if abs(self.avatar_x - text_obj["x"]) < 10 and abs(70 - text_obj["y"]) < 10:
                        self.score -= 40  # ステージ2では得点を減少
                        self.text_objects.remove(text_obj)
                        self.add_text_object()
                                           

            # ステージ1でスコアが-9999以下になった場合、特別な画面を表示
            if self.score <= -9999 and self.game_stage == 1:
                self.show_message_screen = True
                return

            if self.game_end_time is not None and current_frame >= self.game_end_time:
                self.game_ended = True  # ゲーム終了フラグを設定

        # スコアボード表示時もアバターの位置を更新
        if self.game_ended and pyxel.btn(pyxel.KEY_SPACE):
            self.reset_game(next_stage=False)

        # 残り時間の計算
        if self.game_end_time is not None and not self.game_ended:
            self.remaining_time = max(0, (self.game_end_time - current_frame) / 30)  # 残り時間（秒）

    def draw(self):
        pyxel.cls(0)

        if self.show_message_screen:
            pyxel.text(8, 40, "what are you?", 8)
            pyxel.text(22, 60, "[THINK]", 9)
            return

        # ステージに応じたアバターの描画（カウントダウン中も描画）
        if self.game_stage == 1:
            if self.current_avatar_image == 0:
                pyxel.blt(self.avatar_x, 70, 0, 0, 0, 14, 13, 0)  # アバター画像1
            else:
                pyxel.blt(self.avatar_x, 70, 0, 16, 0, 14, 13, 0)  # アバター画像2
        elif self.game_stage == 2:
            if self.current_avatar_image == 0:
                pyxel.blt(self.avatar_x, 70, 0, 32, 0, 14, 13, 0)  # 別のアバター画像1
            else:
                pyxel.blt(self.avatar_x, 70, 0, 48, 0, 14, 13, 0)  # 別のアバター画像2

        if not self.game_started:
            # ゲーム開始前のカウントダウン表示
            pyxel.text(20, 40, f"Start in {self.countdown}", pyxel.COLOR_WHITE)
            
            # ステージに応じた待機画面の表示
            if self.game_stage == 1:
                pyxel.text(5, 30, "Slide mouse.", pyxel.COLOR_WHITE)
            elif self.game_stage == 2:
                pyxel.text(5, 30, "come with me!", 9)
        else:
            if self.game_ended:
                # ゲーム終了時のスコアボード表示（ステージに応じた表示）
                pyxel.text(5, 40, f"Score: {self.score}", pyxel.COLOR_RED)

                if self.game_stage == 1:
                    # ステージ1ではスコアに応じたコメント表示
                    if self.score >= 5900:
                        comment = "seriously?"
                        comment_color = 11
                    elif self.score >= 4000:
                        comment = "Amazing!"
                        comment_color = 11
                    elif self.score >= 0:
                        comment = "That's a lot :)"
                        comment_color = 11
                    elif self.score <= -6000:
                        comment = "almost there."
                        comment_color = 9                 
                    else:
                        comment = "That happens."
                        comment_color = 11

                    # 改行処理を削除して1行で表示
                    pyxel.text(5, 50, comment, comment_color)

                pyxel.text(5, 60, "[SPACE to Again]", pyxel.COLOR_WHITE)
            else:
                # ゲーム中の描画処理
                # 花弁の描画
                for petal in self.petals:
                    pyxel.blt(petal["x"], petal["y"], 0, 0, 32, 8, 10, 0)

                # 桜エビの描画（ステージ1のみ）
                if self.game_stage == 1:
                    for shrimp in self.shrimps:
                        x, y, w, h, _ = shrimp["graphic"]
                        pyxel.blt(shrimp["x"], shrimp["y"], 0, x, y, w, h, 0)

                # 文字オブジェクトの描画（ステージ2のみ）
                if self.game_stage == 2:
                    for text_obj in self.text_objects:
                        x, y, w, h = text_obj["graphic"]
                        pyxel.blt(text_obj["x"], text_obj["y"], 0, x, y, w, h, 0)

                # スコアの表示
                pyxel.text(5, 90, f"Score: {self.score}", pyxel.COLOR_WHITE)

                # 残り時間の表示
                pyxel.text(30, 0, f"{int(self.remaining_time)}s", pyxel.COLOR_WHITE)

APP()
