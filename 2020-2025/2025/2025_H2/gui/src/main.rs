// src/main.rs

use iced::widget::{button, checkbox, column, container, row, scrollable, text, text_input};
use iced::{executor, theme, Application, Command, Element, Font, Length, Settings, Theme};

// The main entry point of the application
pub fn main() -> iced::Result {
    ToDoList::run(Settings {
        // You can customize window settings here
        ..Settings::default()
    })
}

// Represents the main state of our To-Do list application
#[derive(Debug, Default)]
struct ToDoList {
    tasks: Vec<Task>,
    input_value: String,
    filter: Filter,
}

// Represents a single task in our list
#[derive(Debug, Clone)]
struct Task {
    description: String,
    completed: bool,
}

// Defines the different ways we can filter the tasks
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
enum Filter {
    #[default]
    All,
    Active,
    Completed,
}

// Defines all the possible messages (events) that can occur in the application
#[derive(Debug, Clone)]
enum Message {
    InputChanged(String),
    AddTask,
    TaskToggled(usize, bool),
    FilterChanged(Filter),
    DeleteTask(usize),
}

// This is where we implement the core logic for our application
impl Application for ToDoList {
    type Executor = executor::Default;
    type Message = Message;
    type Theme = Theme;
    type Flags = ();

    // The constructor for our application
    fn new(_flags: ()) -> (Self, Command<Message>) {
        (Self::default(), Command::none())
    }

    // The title of the window
    fn title(&self) -> String {
        String::from("Cool To-Do List")
    }

    // The update logic: handles messages and updates the state
    fn update(&mut self, message: Message) -> Command<Message> {
        match message {
            Message::InputChanged(value) => {
                self.input_value = value;
            }
            Message::AddTask => {
                // Only add a task if the input is not empty
                if !self.input_value.is_empty() {
                    self.tasks.push(Task {
                        description: self.input_value.clone(),
                        completed: false,
                    });
                    self.input_value.clear();
                }
            }
            Message::TaskToggled(i, is_checked) => {
                if let Some(task) = self.tasks.get_mut(i) {
                    task.completed = is_checked;
                }
            }
            Message::FilterChanged(filter) => {
                self.filter = filter;
            }
            Message::DeleteTask(i) => {
                if i < self.tasks.len() {
                    self.tasks.remove(i);
                }
            }
        }
        Command::none()
    }

    // The view logic: creates the UI from the current state
    fn view(&self) -> Element<Message> {
        let title = text("To-Do List").size(40);

        // Input field and "Add" button
        let input = text_input("What needs to be done?", &self.input_value)
            .on_input(Message::InputChanged)
            .on_submit(Message::AddTask)
            .padding(10);

        let add_button = button(text("Add").size(20))
            .on_press(Message::AddTask)
            .padding(10)
            .style(theme::Button::Primary);

        // Filter buttons
        let filter_buttons = row![
            button(text("All"))
                .on_press(Message::FilterChanged(Filter::All))
                .style(if self.filter == Filter::All {
                    theme::Button::Primary
                } else {
                    theme::Button::Secondary
                }),
            button(text("Active"))
                .on_press(Message::FilterChanged(Filter::Active))
                .style(if self.filter == Filter::Active {
                    theme::Button::Primary
                } else {
                    theme::Button::Secondary
                }),
            button(text("Completed"))
                .on_press(Message::FilterChanged(Filter::Completed))
                .style(if self.filter == Filter::Completed {
                    theme::Button::Primary
                } else {
                    theme::Button::Secondary
                })
        ]
        .spacing(10);

        // The list of tasks
        let tasks: Element<Message> = self
            .tasks
            .iter()
            .enumerate()
            .filter(|(_i, task)| match self.filter {
                Filter::All => true,
                Filter::Active => !task.completed,
                Filter::Completed => task.completed,
            })
            .fold(column![].spacing(5), |col, (i, task)| {
                let task_row = row![
                    checkbox(&task.description, task.completed)
                        .on_toggle(move |is_checked| Message::TaskToggled(i, is_checked))
                        .text_size(22),
                    button(text("X"))
                        .on_press(Message::DeleteTask(i))
                        .style(theme::Button::Destructive)
                        .padding(5),
                ]
                .spacing(20)
                .align_items(iced::Alignment::Center);

                col.push(task_row)
            })
            .into();

        // The main layout of the application
        let content = column![
            title,
            row![input, add_button].spacing(10),
            filter_buttons,
            scrollable(container(tasks).padding(10))
        ]
        .spacing(20)
        .padding(20)
        .max_width(600);

        // Center the main content in a container
        container(content)
            .width(Length::Fill)
            .height(Length::Fill)
            .center_x()
            .center_y()
            .into()
    }

    // Set the custom dark theme
    fn theme(&self) -> Theme {
        Theme::Dark
    }
}
