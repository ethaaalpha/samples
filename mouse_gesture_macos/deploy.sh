#!/bin/sh

set -e

echo "Building package"
cargo build --release

echo "Creating log folder"
mkdir -p ~/.macos_gesture

echo "Deploying binary"
sudo cp target/release/macos_gesture /usr/local/bin/macos_gesture

echo "Deploying start-up service"
cat > ~/Library/LaunchAgents/macos_gesture.plist <<EOF

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>Label</key>
		<string>macos_gesture</string>
		<key>ProgramArguments</key>
		<array>
			<string>/usr/local/bin/macos_gesture</string>
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
