# Why ?
This project is designed to replace the legacy `LogiOptions+` app. This one sucks since few months and is too heavy for only handling mouse events.  

### How to use ?
You'll need `rust` and `cargo` to be installed.  
Then just run `deploy.sh` and restart your computer!

> [!NOTE]
> You can edit properties inside the `deploy.sh` file

> [!TIP]
> If you want to update the script, just edit the code and run `update.sh` it will recompile and update the current bin (a restart may be needed)

#### Specifications
The program support:
- the option `--drag`: which active changing desktops by holding middle button and moving mouse
- the option `--scroll`: which reverse the scroll of the mouse only (not the trackpad)
