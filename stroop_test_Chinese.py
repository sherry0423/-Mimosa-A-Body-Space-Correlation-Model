import tkinter as tk
from tkinter import messagebox, font
import random
import time
import pandas as pd
from datetime import datetime


class StroopTest:
    def __init__(self, root):
        self.root = root
        self.root.title("斯特鲁普任务测试")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # 设置字体
        self.default_font = font.Font(family="SimHei", size=12)
        self.word_font = font.Font(family="SimHei", size=60)
        self.score_font = font.Font(family="SimHei", size=16, weight="bold")

        # 测试数据
        self.colors = ["红色", "绿色", "蓝色", "黄色", "紫色"]
        self.english_colors = ["红", "绿", "蓝", "黄", "紫"]
        self.color_codes = {
            "红色": "#FF0000",
            "绿色": "#00FF00",
            "蓝色": "#0000FF",
            "黄色": "#FFFF00",
            "紫色": "#800080"
        }
        self.english_color_codes = {
            "红": "#FF0000",
            "绿": "#00FF00",
            "蓝": "#0000FF",
            "黄": "#FFFF00",
            "紫": "#800080"
        }

        # 测试状态
        self.trials = []
        self.current_trial = 0
        self.start_time = 0
        self.test_started = False
        self.results = []
        self.score = 0  # 新增：当前得分

        # 创建界面
        self.create_widgets()

        # 生成测试序列
        self.generate_trials()

    def create_widgets(self):
        # 欢迎页
        self.welcome_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            self.welcome_frame,
            text="斯特鲁普任务测试",
            font=font.Font(family="SimHei", size=24, weight="bold"),
            bg="#f0f0f0"
        ).pack(pady=50)

        instructions = """
        欢迎参加斯特鲁普任务测试！

        在这个测试中，你将看到用不同颜色书写的颜色词。
        你的任务是尽快判断文字的颜色，而不是文字本身的含义。

        例如：
        - 如果看到用红色书写的"蓝"，你应该按红色对应的按钮。
        - 如果看到用绿色书写的"黄"，你应该按绿色对应的按钮。

        请在保证准确性的前提下，尽可能快速地做出反应。

        测试规则：
        - 每正确回答一个得1分
        - 每错误回答一个扣5分

        测试将分为练习和正式两个阶段，每个阶段包含多个试次。

        准备好了吗？点击"开始练习"按钮开始！
        """

        tk.Label(
            self.welcome_frame,
            text=instructions,
            font=self.default_font,
            bg="#f0f0f0",
            justify=tk.LEFT,
            wraplength=600
        ).pack(pady=30)

        self.start_practice_btn = tk.Button(
            self.welcome_frame,
            text="开始练习",
            font=self.default_font,
            bg="#4CAF50",
            fg="white",
            command=self.start_practice,
            width=15,
            height=2
        )
        self.start_practice_btn.pack(pady=20)

        # 测试页
        self.test_frame = tk.Frame(self.root, bg="#f0f0f0")

        # 新增：得分显示
        self.word_label = tk.Label(
            self.test_frame,
            text="",
            font=self.word_font,
            bg="#f0f0f0"
        )
        self.word_label.pack(pady=60)

        self.instruction_label = tk.Label(
            self.test_frame,
            text="请选择字的颜色:",
            font=self.default_font,
            bg="#f0f0f0"
        )
        self.instruction_label.pack(pady=20)

        self.buttons_frame = tk.Frame(self.test_frame, bg="#f0f0f0")
        self.buttons_frame.pack(pady=20)

        self.color_buttons = []
        for color in self.colors:
            button = tk.Button(
                self.buttons_frame,
                text=color,
                font=self.default_font,
                bg=self.color_codes[color],
                fg="white",
                width=10,
                command=lambda c=color: self.on_color_click(c)
            )
            button.pack(side=tk.LEFT, padx=10)
            self.color_buttons.append(button)

        # 新增：Stop按钮
        self.stop_btn = tk.Button(
            self.test_frame,
            text="Stop",
            font=self.default_font,
            bg="#f44336",
            fg="white",
            command=self.stop_test,
            width=10,
            height=1
        )
        self.stop_btn.pack(pady=20)

        # 结果页
        self.results_frame = tk.Frame(self.root, bg="#f0f0f0")

        self.results_label = tk.Label(
            self.results_frame,
            text="测试结果",
            font=font.Font(family="SimHei", size=24, weight="bold"),
            bg="#f0f0f0"
        )
        self.results_label.pack(pady=30)

        self.results_text = tk.Text(
            self.results_frame,
            font=self.default_font,
            width=60,
            height=15,
            bg="white"
        )
        self.results_text.pack(pady=20)
        self.results_text.config(state=tk.DISABLED)

        self.save_btn = tk.Button(
            self.results_frame,
            text="保存结果",
            font=self.default_font,
            bg="#2196F3",
            fg="white",
            command=self.save_results,
            width=15,
            height=2
        )
        self.save_btn.pack(pady=10)

        self.restart_btn = tk.Button(
            self.results_frame,
            text="重新开始",
            font=self.default_font,
            bg="#f44336",
            fg="white",
            command=self.restart_test,
            width=15,
            height=2
        )
        self.restart_btn.pack(pady=10)

    def generate_trials(self):
        # 生成练习试次：10个一致和10个不一致
        practice_trials = []
        for _ in range(5):
            for word in self.english_colors:
                # 一致试次
                practice_trials.append({
                    "word": word,
                    "color": word,
                    "type": "congruent",
                    "is_practice": True
                })
                # 不一致试次（随机选择不同颜色）
                colors = [c for c in self.english_colors if c != word]
                color = random.choice(colors)
                practice_trials.append({
                    "word": word,
                    "color": color,
                    "type": "incongruent",
                    "is_practice": True
                })

        # 生成正式试次：每种类型20个
        trials = []
        for _ in range(20):
            for word in self.english_colors:
                # 一致试次
                trials.append({
                    "word": word,
                    "color": word,
                    "type": "congruent",
                    "is_practice": False
                })
                # 不一致试次
                colors = [c for c in self.english_colors if c != word]
                color = random.choice(colors)
                trials.append({
                    "word": word,
                    "color": color,
                    "type": "incongruent",
                    "is_practice": False
                })
                # 中性试次（用黑色显示颜色词）
                # trials.append({
                #     "word": word,
                #     "color": "Black",
                #     "type": "neutral",
                #     "is_practice": False
                # })

        # 随机打乱试次顺序
        random.shuffle(practice_trials)
        random.shuffle(trials)

        # 合并试次，练习在前，正式在后
        self.trials = practice_trials + trials

    def start_practice(self):
        self.welcome_frame.pack_forget()
        self.test_frame.pack(fill=tk.BOTH, expand=True)
        self.current_trial = 0
        self.test_started = True
        self.show_trial()

    def show_trial(self):
        if self.current_trial < len(self.trials):
            trial = self.trials[self.current_trial]

            # 显示注视点
            # self.word_label.config(text="+", fg="black")
            # self.root.update()
            # time.sleep(0.1)  # 1秒注视点

            # 显示试次
            if trial["color"] == "Black":
                color_code = "#000000"
            else:
                color_code = self.english_color_codes[trial["color"]]

            self.word_label.config(text=trial["word"], fg=color_code)
            self.start_time = time.time()
        else:
            self.end_test()

    def on_color_click(self, selected_color):
        if not self.test_started:
            return

        end_time = time.time()
        reaction_time = end_time - self.start_time
        trial = self.trials[self.current_trial]

        # 记录结果
        correct = False
        if trial["color"] == "Black":
            # 中性试次不计分
            correct = None
        else:
            # 检查回答是否正确
            english_color_map = {
                "红色": "红",
                "绿色": "绿",
                "蓝色": "蓝",
                "黄色": "黄",
                "紫色": "紫"
            }
            correct = (english_color_map[selected_color] == trial["color"])

            # 新增：计分逻辑
            if correct:
                self.score += 1
            else:
                self.score -= 5

        self.results.append({
            "trial_number": self.current_trial + 1,
            "word": trial["word"],
            "display_color": trial["color"],
            "response_color": selected_color,
            "is_correct": correct,
            "reaction_time": reaction_time,
            "trial_type": trial["type"],
            "is_practice": trial["is_practice"],
            "score": self.score  # 新增：记录当前得分
        })

        # 直接进入下一个试次，不显示反馈
        self.current_trial += 1
        self.show_trial()

    def stop_test(self):
        if messagebox.askyesno("确认", "确定要结束测试吗？当前得分将被保存。"):
            self.end_test()

    def end_test(self):
        self.test_started = False
        self.test_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        # 计算结果统计
        practice_results = [r for r in self.results if r["is_practice"]]
        test_results = [r for r in self.results if not r["is_practice"]]

        # 练习阶段统计
        practice_correct = [r for r in practice_results if r["is_correct"]]
        practice_accuracy = len(practice_correct) / len(practice_results) * 100 if practice_results else 0
        practice_rt = sum(r["reaction_time"] for r in practice_results) / len(
            practice_results) if practice_results else 0

        # 测试阶段统计
        test_correct = [r for r in test_results if r["is_correct"]]
        test_accuracy = len(test_correct) / len(test_results) * 100 if test_results else 0

        # 按类型分类统计
        congruent_trials = [r for r in test_results if r["trial_type"] == "congruent" and r["is_correct"]]
        incongruent_trials = [r for r in test_results if r["trial_type"] == "incongruent" and r["is_correct"]]
        neutral_trials = [r for r in test_results if r["trial_type"] == "neutral" and r["is_correct"]]

        congruent_rt = sum(r["reaction_time"] for r in congruent_trials) / len(
            congruent_trials) if congruent_trials else 0
        incongruent_rt = sum(r["reaction_time"] for r in incongruent_trials) / len(
            incongruent_trials) if incongruent_trials else 0
        neutral_rt = sum(r["reaction_time"] for r in neutral_trials) / len(neutral_trials) if neutral_trials else 0

        # 计算斯特鲁普效应
        stroop_effect = incongruent_rt - congruent_rt

        # 显示结果
        result_text = f"""
        测试完成！

        最终得分: {self.score}

        练习阶段:
          准确率: {practice_accuracy:.2f}%
          平均反应时间: {practice_rt:.2f}秒

        正式测试:
          总体准确率: {test_accuracy:.2f}%

        按类型分类的平均反应时间:
          - 一致试次: {congruent_rt:.2f}秒
          - 不一致试次: {incongruent_rt:.2f}秒
          - 中性试次: {neutral_rt:.2f}秒

        斯特鲁普效应: {stroop_effect:.2f}秒

        斯特鲁普效应反映了不一致试次和一致试次之间的反应时间差异。
        差异越大，表明语义干扰对颜色判断的影响越强。
        """

        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, result_text)
        self.results_text.config(state=tk.DISABLED)

    def save_results(self):
        try:
            # 创建数据框
            df = pd.DataFrame(self.results)

            # 保存为CSV文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"stroop_test_results_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding="utf-8-sig")

            messagebox.showinfo("成功", f"结果已保存至 {filename}")
        except Exception as e:
            messagebox.showerror("错误", f"保存结果时出错: {str(e)}")

    def restart_test(self):
        # 重置测试状态
        self.trials = []
        self.current_trial = 0
        self.start_time = 0
        self.test_started = False
        self.results = []
        self.score = 0

        # 生成新的测试序列
        self.generate_trials()

        # 显示欢迎页
        self.results_frame.pack_forget()
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = StroopTest(root)
    root.mainloop()