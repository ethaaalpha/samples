#!/bin/bash

cargo build --release
cp target/release/macos_gesture Macos_Gesture.app/Contents/MacOS/macos_gesture
codesign --force --deep --sign - Macos_Gesture.app
mv Macos_Gesture.app /Applications/
