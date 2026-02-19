use std::sync::atomic::AtomicBool;
use std::vec;

use core_foundation::runloop::{CFRunLoop, kCFRunLoopCommonModes};
use core_graphics::event::{CGEvent, CGEventFlags, CGKeyCode, EventField};
use core_graphics::event::{
    CGEventTap, CGEventTapLocation, CGEventTapOptions, CGEventTapPlacement, CGEventTapProxy,
    CGEventType, CallbackResult,
};
use core_graphics::event_source::CGEventSource;
use core_graphics::event_source::CGEventSourceStateID;

// see: https://www.sheshbabu.com/posts/rust-module-system/
mod structs;
use structs::{Actions, Options};

mod consts;
use consts::{NOT_AUTHORIZED, SYS_ERROR};

static APP_OPTS: Options = Options {
    reverse_scroll: false,
    drag_manager: true,
    drag_trigger: 20,
};

static CONSUMED: AtomicBool = AtomicBool::new(false);

fn handle_scroll_wheel(event: &CGEvent) -> CallbackResult {
    let vertical_axis = event.get_integer_value_field(EventField::SCROLL_WHEEL_EVENT_DELTA_AXIS_1);

    event.set_integer_value_field(EventField::SCROLL_WHEEL_EVENT_DELTA_AXIS_1, -vertical_axis);
    return CallbackResult::Keep;
}

fn build_event(keycode: CGKeyCode, down: bool, ctrl: bool) -> CGEvent {
    let source = CGEventSource::new(CGEventSourceStateID::CombinedSessionState).expect(SYS_ERROR);
    let event = CGEvent::new_keyboard_event(source.clone(), keycode, down).expect(SYS_ERROR);

    if ctrl {
        let mut existing_flags = event.get_flags();

        existing_flags.insert(CGEventFlags::CGEventFlagControl);
        event.set_flags(existing_flags);
    }
    return event;
}

fn switch_desktops(action: Actions) {
    let keycode = action.key_code();

    let down = build_event(keycode, true, true);
    down.post(CGEventTapLocation::HID);

    let up = build_event(keycode, false, false);
    up.post(CGEventTapLocation::HID);

    CONSUMED.store(true, std::sync::atomic::Ordering::Relaxed);
}

// event related to press the middle button + dragg
fn handle_mousse_other_drag(event: &CGEvent) -> CallbackResult {
    if CONSUMED.load(std::sync::atomic::Ordering::Relaxed) {
        return CallbackResult::Keep;
    }
    let delta_x = event.get_integer_value_field(EventField::MOUSE_EVENT_DELTA_X);
    let delta_y = event.get_integer_value_field(EventField::MOUSE_EVENT_DELTA_Y);

    if delta_x.abs() > delta_y.abs() && delta_x.abs() > APP_OPTS.drag_trigger {
        // horizontal
        if delta_x > 0 {
            switch_desktops(Actions::SwipeRight);
        } else {
            switch_desktops(Actions::SwipeLeft);
        }
    } else if delta_y.abs() > APP_OPTS.drag_trigger {
        // vertical
        if delta_y > 0 {
            switch_desktops(Actions::SwipeBottom);
        } else {
            switch_desktops(Actions::SwipeTop);
        }
    }
    return CallbackResult::Keep;
}

fn mouse_handler(
    _proxy: CGEventTapProxy,
    event_type: CGEventType,
    event: &CGEvent,
) -> CallbackResult {
    match event_type {
        CGEventType::ScrollWheel if APP_OPTS.reverse_scroll => {
            return handle_scroll_wheel(event);
        }
        CGEventType::OtherMouseDragged if APP_OPTS.drag_manager => {
            return handle_mousse_other_drag(event);
        }
        CGEventType::OtherMouseUp if APP_OPTS.drag_manager => {
            CONSUMED.store(false, std::sync::atomic::Ordering::Relaxed);
            return CallbackResult::Keep;
        }
        _ => {
            return CallbackResult::Keep;
        }
    }
}

fn runner() {
    let event_tap = CGEventTap::new(
        CGEventTapLocation::HID,
        CGEventTapPlacement::HeadInsertEventTap,
        CGEventTapOptions::Default,
        vec![
            CGEventType::ScrollWheel,
            CGEventType::OtherMouseDragged,
            CGEventType::OtherMouseUp,
        ],
        mouse_handler,
    )
    .expect(NOT_AUTHORIZED);
    let event_source = event_tap
        .mach_port()
        .create_runloop_source(0)
        .expect(NOT_AUTHORIZED);

    unsafe {
        CFRunLoop::get_current().add_source(&event_source, kCFRunLoopCommonModes);
    }

    CFRunLoop::run_current();
}

fn main() {
    runner();
}
