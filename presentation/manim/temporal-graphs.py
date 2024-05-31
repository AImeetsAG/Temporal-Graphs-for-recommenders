from manim import *

np.random.seed(0)
def generate_random_array():
    while True:
        array = np.random.choice([0, *range(1, 100)], size=(3, 3), p=[0.2] + [0.8 / 99] * 99)
        if np.all(array.sum(axis=1) <= 100):
            return array

m, n = 10, 7

random_arrays = {j: {} for j in range(n)}
sum_random_arrays = {j: {} for j in range(n)}
sum_sum_random_arrays = {j: {} for j in range(n)}
matrix_elements = {j: {} for j in range(n)}
matrix_sum_elements = {j: {} for j in range(n)}
matrix_sum_sum_elements = {j: {} for j in range(n)}
matrix_batch = {j : {}  for j in range(n)}

for j in range(n):
    for i in range(m):
        random_arrays[j][i] = generate_random_array()/100
        rnd = random_arrays[j][i]
        matrix_elements[j][i] = [
            [f"{rnd[0,0]:.2f}", f"{rnd[0,1]:.2f}", r"\cdots", f"{rnd[0,2]:.2f}"],
            [f"{rnd[1,0]:.2f}", f"{rnd[1,1]:.2f}", r"\cdots", f"{rnd[1,2]:.2f}"],
            [r"\vdots", r"\vdots", r"\ddots",  r"\vdots"],
            [f"{rnd[2,0]:.2f}", f"{rnd[2,1]:.2f}", r"\cdots", f"{rnd[2,2]:.2f}"],
        ]

    for i in reversed(range(m)):
        sum_random_arrays[j][i] = sum([random_arrays[j][k] for k in range(i,m)])
        rnd = sum_random_arrays[j][i]
        matrix_sum_elements[j][i] = [
            [f"{rnd[0, 0]:.2f}", f"{rnd[0, 1]:.2f}", r"\cdots", f"{rnd[0, 2]:.2f}"],
            [f"{rnd[1, 0]:.2f}", f"{rnd[1, 1]:.2f}", r"\cdots", f"{rnd[1, 2]:.2f}"],
            [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
            [f"{rnd[2, 0]:.2f}", f"{rnd[2, 1]:.2f}", r"\cdots", f"{rnd[2, 2]:.2f}"],
        ]

for j in range(n):
    sum_sum_random_arrays[j] = sum([sum_random_arrays[k][0] for k in range(j, n)])
    rnd = sum_sum_random_arrays[j]
    matrix_sum_sum_elements[j] = [
        [f"{rnd[0, 0]:.2f}", f"{rnd[0, 1]:.2f}", r"\cdots", f"{rnd[0, 2]:.2f}"],
        [f"{rnd[1, 0]:.2f}", f"{rnd[1, 1]:.2f}", r"\cdots", f"{rnd[1, 2]:.2f}"],
        [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
        [f"{rnd[2, 0]:.2f}", f"{rnd[2, 1]:.2f}", r"\cdots", f"{rnd[2, 2]:.2f}"],
    ]

nm = sum_sum_random_arrays[0]/sum_sum_random_arrays[0].sum(axis=1, keepdims=True)
normalized_array_elements = [
        [f"{nm[0, 0]:.2f}", f"{nm[0, 1]:.2f}", r"\cdots", f"{nm[0, 2]:.2f}"],
        [f"{nm[1, 0]:.2f}", f"{nm[1, 1]:.2f}", r"\cdots", f"{nm[1, 2]:.2f}"],
        [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
        [f"{nm[2, 0]:.2f}", f"{nm[2, 1]:.2f}", r"\cdots", f"{nm[2, 2]:.2f}"],
    ]

class array(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        line_for_spacing = Text(r"AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz \frac{0}{0}")
        line_for_spacing2 = Tex("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")
        line_buff = 0.25
        line_skip = max(line_for_spacing.height, line_for_spacing2.height) + line_buff

        outer_offset = np.array([1, 0.5, 0])
        offset = np.array([0.5, 0.25, 0])
        for j in range(n):
            for i, matrix_ in matrix_elements[j].items():
                matrix = Matrix(matrix_, element_alignment_corner=DL).set_color(BLACK)
                matrix.to_edge(UR)
                position = matrix.get_center() - j*outer_offset - i*offset
                background = BackgroundRectangle(matrix, fill_opacity=1,
                                                 fill_color=WHITE)
                matrix_group = VGroup(background, matrix)
                matrix_group.move_to(position)
                self.add(matrix_group)
                matrix_batch[j][i] = matrix_group

                if i + j  == 0:
                    under_brace = Brace(mobject=matrix).set_color(BLACK)
                    under_brace_text = under_brace.get_text("513 genres").set_color(BLACK)
                    left_brace = Brace(mobject=matrix,direction=LEFT).set_color(BLACK)
                    left_brace_text = left_brace.get_text("992 users").set_color(BLACK)
                    self.add(left_brace, left_brace_text)
                    self.play(GrowFromCenter(under_brace),
                              GrowFromCenter(left_brace),
                              FadeIn(under_brace_text),
                              FadeIn(left_brace_text), run_time=1/2)
                    brace_group = VGroup(under_brace,
                                         under_brace_text,
                                         left_brace,
                                         left_brace_text)
                    rnd = random_arrays[j][i]
                    u = 1
                    explain_txt = [MarkupText(f"User <span fgcolor='#26a69a'>{u + 513}</span> listens to song that is: ", color=BLACK)]
                    explain_txt.extend([MarkupText(f"<span fgcolor='#26a69a'>{100*rnd[u,v]:.2f}%</span> genre {v}", color=BLACK) for v in [0,1,]])
                    explain_txt.append(MarkupText("...", color="#26a69a"))
                    explain_txt.append(MarkupText(f"<span fgcolor='#26a69a'>{100*rnd[u,2]:.2f}%</span> genre 512", color=BLACK))
                    explain_txt.append(MarkupText(f"i.e. <span fgcolor='#26a69a'>{100 * rnd[u, 0]:.2f}%</span> of all user tags", color=BLACK))
                    explain_txt.append(MarkupText(f"for this song are genre 0, etc.", color=BLACK))
                    explain = VGroup(*explain_txt).scale(0.5).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
                    self.play(Write(explain[0]),run_time=1)
                    for k in range(1,5):
                        if k == 3:
                            self.add(explain[k],
                                     matrix.get_entries()[3 + k].set_color("#26a69a"))
                        else:
                            self.play(Write(explain[k]),
                                      matrix.get_entries()[3 + k].animate.set_color("#26a69a"),
                                      run_time=1/2)
                    self.play(Write(explain[5]),run_time=1)
                    self.play(Write(explain[6]),run_time=1/2)
                    self.wait(1/2)
                    self.play(FadeOut(explain),
                              FadeOut(brace_group),
                              *[matrix.get_entries()[3 + k].animate.set_color(BLACK) for k in range(1,5)])
                    
                if j == 0 and i == 1:
                    item = ["Continuous stream of data",
                            "Each sec for 1587 days"]
                    blist = BulletedList(item[0],
                                         item[1]).set_color(BLACK).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
                    self.play(Write(blist[0]), run_time=1/(j ** 2 + 2))
                elif j == 0 and i == 2:
                    self.play(Write(blist[1]), run_time=1/(j ** 2 + 2))
                elif j == 0 and i == m - 2:
                    self.play(FadeOut(blist), run_time=1/(j ** 2 + 2))
                else:
                    self.wait(1 / (j ** 2 + 2))

            for i in reversed(range(m)):
                matrix_sum_ = matrix_sum_elements[j][i]
                matrix_sum = Matrix(matrix_sum_, element_alignment_corner=DL).set_color(BLACK)
                background = BackgroundRectangle(matrix_sum, fill_opacity=1,
                                                 fill_color=WHITE)
                matrix_sum_group = VGroup(background, matrix_sum)

                matrix_group = matrix_batch[j][i]
                position = matrix_group.get_center()
                matrix_sum_group.move_to(position)

                self.add(matrix_sum_group)
                self.remove(matrix_group)

                if j == 0 and i == m - 1:
                    item = ["Discretize: partition by day",
                            "Sum over each day"]
                    blist2 = BulletedList(item[0],
                                          item[1]).set_color(BLACK).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
                    self.play(Write(blist2[0]),
                              matrix_sum_group.animate.shift(offset), run_time=1 / (j ** 3 + 2))
                    self.remove(matrix_batch[j][i - 1])
                    matrix_batch[j][i - 1] = matrix_sum_group
                elif j == 0 and i == m - 2:
                    self.play(Write(blist2[1]),
                              matrix_sum_group.animate.shift(offset), run_time=1 / (j ** 3 + 2))
                    self.remove(matrix_batch[j][i - 1])
                    matrix_batch[j][i - 1] = matrix_sum_group
                elif j == 3 and i == m - 1:
                    self.play(FadeOut(blist2),
                              matrix_sum_group.animate.shift(offset), run_time=1 / (j ** 3 + 2))
                    self.remove(blist2)
                    self.remove(matrix_batch[j][i - 1])
                    matrix_batch[j][i - 1] = matrix_sum_group
                elif i > 0:
                    self.play(matrix_sum_group.animate.shift(offset), run_time=1 / (j ** 3 + 2))
                    self.remove(matrix_batch[j][i - 1])
                    matrix_batch[j][i - 1] = matrix_sum_group
                else:
                    self.add(matrix_sum_group)
                    self.remove(matrix_batch[j][i])
                    matrix_batch[j][i] = matrix_sum_group

            self.wait(1/(j + 1))

        self.wait(1)

        for j in reversed(range(n)):
            matrix_sum_sum_ = matrix_sum_sum_elements[j]
            matrix_sum_sum = Matrix(matrix_sum_sum_, element_alignment_corner=DL).set_color(BLACK)

            background = BackgroundRectangle(matrix_sum_sum, fill_opacity=1,
                                             fill_color=WHITE)
            matrix_sum_sum_group = VGroup(background, matrix_sum_sum)

            matrix_sum_group = matrix_batch[j][0]
            position = matrix_sum_group.get_center()

            matrix_sum_sum_group.move_to(position)

            self.add(matrix_sum_sum_group)
            self.remove(matrix_sum_group)

            if j == n - 1:
                item = ["Sum over week-long window",
                        "Normalize by column sum"]
                blist3 = BulletedList(item[0],
                                      item[1]).set_color(BLACK).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
                self.play(Write(blist3[0]),
                          matrix_sum_sum_group.animate.shift(outer_offset), run_time=1 /((n - 1 - j) + 2))
                self.remove(matrix_batch[j - 1][0])
                matrix_batch[j - 1][0] = matrix_sum_sum_group
            elif j > 0:
                self.play(matrix_sum_sum_group.animate.shift(outer_offset), run_time=1 / ((n - 1 - j) + 2))
                self.remove(matrix_batch[j - 1][0])
                matrix_batch[j - 1][0] = matrix_sum_sum_group
            else:
                self.add(matrix_sum_sum_group)
                self.remove(matrix_batch[j][0])
                matrix_batch[j][0] = matrix_sum_sum_group

                matrix_normalized_ = normalized_array_elements
                matrix_normalized = Matrix(matrix_normalized_, element_alignment_corner=DL).set_color(BLACK)

                background = BackgroundRectangle(matrix_normalized, fill_opacity=1,
                                                 fill_color=WHITE)

                matrix_normalized_group = VGroup(background, matrix_normalized)
                position = matrix_sum_sum_group.get_center()
                matrix_normalized_group.move_to(position)

                self.play(Write(blist3[1]), run_time=1/2)
                self.wait(1)
                self.play(FadeOut(matrix_sum_sum),
                          FadeIn(matrix_normalized), run_time=1)
                
        self.wait(5)
