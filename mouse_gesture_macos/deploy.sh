#!/bin/sh

set -e

echo "Building package"
cargo build --release

mkdir -p Macos_Gesture.app/Contents/MacOS
cp target/release/macos_gesture Macos_Gesture.app/Contents/MacOS/macos_gesture
chmod +x Macos_Gesture.app/Contents/MacOS/macos_gesture

cat > Macos_Gesture.app/Contents/Info.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Macos_Gesture</string>

    <key>CFBundleDisplayName</key>
    <string>Macos_Gesture</string>

    <key>CFBundleIdentifier</key>
    <string>com.ethaaalpha.macos_gesture</string>

    <key>CFBundleExecutable</key>
    <string>macos_gesture</string>

    <key>CFBundlePackageType</key>
    <string>APPL</string>

    <key>CFBundleVersion</key>
    <string>1.0</string>

    <key>CFBundleShortVersionString</key>
    <string>1.0</string>

    <key>LSMinimumSystemVersion</key>
    <string>11.0</string>
</dict>
</plist>
EOF
codesign --force --deep --sign - Macos_Gesture.app

echo "Deploying"
mv Macos_Gesture.app /Applications/

echo "Creating log folder"
mkdir -p ~/.macos_gesture
# 
echo "Deploying start-up service"
cat > ~/Library/LaunchAgents/com.ethaaalpha.macos_gesture.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>Label</key>
		<string>com.ethaaalpha.macos_gesture</string>
		<key>ProgramArguments</key>
		<array>
			<string>/Applications/Macos_Gesture.app/Contents/MacOS/macos_gesture</string>
			<string>--scroll</string>
			<string>--drag</string>
		</array>
		<key>StandardOutPath</key>
		<string>/Users/ethaaalpha/.macos_gesture/out.log</string>
		<key>StandardErrorPath</key>
		<string>/Users/ethaaalpha/.macos_gesture/err.log</string>
		<key>RunAtLoad</key>
		<true/>
	</dict>
</plist>
EOF

# see launchctl on macos
