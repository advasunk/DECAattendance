from calendar import c
import flet as flt
from flet import (
    Page,
    TextField,
    FloatingActionButton,
    Column,
    Row,
    Text,
    IconButton,
    OutlinedButton,
    Tabs,
    Tab,
    UserControl,
    Checkbox,
    colors,
    icons,
)


class Student(UserControl):
    def __init__(self, student_name, student_status_change, student_delete):
        super().__init__()
        self.completed = False
        self.student_name = student_name
        self.student_status_change = student_status_change
        self.student_delete = student_delete

    def build(self):
        self.display_student = Checkbox(
            value=False, label=self.student_name, on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_student,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Edit Student",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Delete Studentt",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Update Students",
                    on_click=self.save_clicked,
                ),
            ],
        )

        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_student.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_student.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.student_delete(self)

    def status_changed(self, e):
        self.completed = self.display_student.value
        self.student_status_change(self)


class MyTodoApp(UserControl):
    def build(self):
        self.new_student = TextField(hint_text="Add a new student here", expand=True)
        self.students = Column()
        self
        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="All"), Tab(text="Absent"), Tab(text="Present")],
        )

        self.items_left = Text("0 students left")

        return Column(
            width=600,
            controls=[
                Row([Text(value="Attendance", style="headlineMedium")], alignment="center"),
                Row(
                    controls=[
                        self.new_student,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.students,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text="Clear present", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        student = Student(self.new_student.value, self.student_status_change, self.student_delete)
        self.students.controls.append(student)
        self.new_student.value = ""
        self.update()

    def student_status_change(self, student):
        self.update()

    def student_delete(self, student):
        self.students.controls.remove(student)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for student in self.students.controls[:]:
            if student.completed:
                self.student_delete(student)

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for student in self.students.controls:
            student.visible = (
                    status == "All"
                    or (status == "Absent" and not student.completed)
                    or (status == "Present" and student.completed)
            )
            if not student.completed:
                count += 1
        self.items_left.value = f"{count} active students(s) left"
        super().update()


def main(page: Page):
    page.title = "DECA Tracker"
    page.horizontal_alignment = "center"

    # creat a TODO app instance
    app = MyTodoApp()

    page.add(app)


flt.app(target=main, view=flt.FLET_APP)
