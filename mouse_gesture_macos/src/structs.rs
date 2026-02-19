use core_graphics::event::{CGKeyCode, KeyCode};

pub enum Actions {
    SwipeRight,
    SwipeLeft,
    SwipeTop,
    SwipeBottom,
}

impl Actions {
    pub fn key_code(&self) -> CGKeyCode {
        match self {
            Actions::SwipeRight => KeyCode::RIGHT_ARROW,
            Actions::SwipeLeft => KeyCode::LEFT_ARROW,
            Actions::SwipeTop => KeyCode::UP_ARROW,
            Actions::SwipeBottom => KeyCode::DOWN_ARROW,
        }
    }
}

pub struct Options {
    pub reverse_scroll: bool,
    pub drag_manager: bool,
}
