import os
import subprocess
import sys
import time
import pyautogui

def open_teams():
    """Opens Microsoft Teams on different operating systems and handles potential issues."""

    try:
        # Windows
        if sys.platform == "win32":
            teams_path = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Teams", "current", "Teams.exe")
            if os.path.exists(teams_path):
                subprocess.Popen([teams_path])
                print("Opening Microsoft Teams on Windows...")
            else:
                # Try alternative path (Update.exe launches the updater, but often leads to Teams)
                teams_path = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Teams", "Update.exe")
                if os.path.exists(teams_path):
                  subprocess.Popen([teams_path, "--processStart", "Teams.exe"])
                  print("Opening Microsoft Teams on Windows (using Update.exe)...")
                else:
                  print("Microsoft Teams not found at standard paths on Windows.")
                  # Attempt to find Teams using the 'where' command (can be slow)
                  try:
                      result = subprocess.run(['where', 'Teams.exe'], capture_output=True, text=True, check=True)
                      teams_path = result.stdout.strip().split('\n')[0] # Take the first path found
                      if os.path.exists(teams_path):
                          subprocess.Popen([teams_path])
                          print(f"Opening Microsoft Teams on Windows from: {teams_path}")
                      else:
                          raise FileNotFoundError("Teams.exe not found from 'where' command output.")
                  except (subprocess.CalledProcessError, FileNotFoundError):
                      print("Failed to find Microsoft Teams executable on Windows.")
                      return False


        # macOS
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "/Applications/Microsoft Teams.app"])
            print("Opening Microsoft Teams on macOS...")

        # Linux (various possibilities, trying common ones)
        elif sys.platform.startswith("linux"):
            try:
                subprocess.Popen(["teams"])  # Try common command
                print("Opening Microsoft Teams on Linux...")
            except FileNotFoundError:
                try:
                    subprocess.Popen(["/usr/bin/teams"]) # Try alternative path
                    print("Opening Microsoft Teams on Linux from /usr/bin/...")
                except FileNotFoundError:
                    try:
                        # Look for a snap installation
                        subprocess.Popen(["snap", "run", "teams"])
                        print("Opening Microsoft Teams on Linux (snap)...")
                    except FileNotFoundError:
                        print("Microsoft Teams not found on Linux. Please ensure it is installed and accessible in your PATH.")
                        return False

        else:
            print("Unsupported operating system.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True


def wait_for_teams_window(timeout=15):
    """
    Waits for the Microsoft Teams window to appear using pyautogui.

    Args:
        timeout: The maximum time (in seconds) to wait for the window.

    Returns:
        True if the window is found within the timeout, False otherwise.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Attempt to find a specific UI element that indicates Teams has loaded.
            # You may need to adjust the coordinates/image based on your Teams version.
            # Use a tool like AutoHotkey's Window Spy to identify UI elements.
            # Example (replace with a reliable UI element location)
            if pyautogui.locateOnScreen('teams_icon.png', confidence=0.8) is not None:  # Use an image of the Teams icon
                print("Microsoft Teams window detected.")
                return True

            #Alternative, looking for the window title
            #if pyautogui.getWindowsWithTitle("Microsoft Teams"):
            #    print("Microsoft Teams window detected.")
            #    return True
        except Exception as e:
            print(f"Error during window detection: {e}")  # Be cautious about excessive printing in a loop
        time.sleep(1)  # Check every 1 second
    print("Timed out waiting for Microsoft Teams window.")
    return False

if __name__ == "__main__":
    if open_teams():
        wait_for_teams_window() # Wait for the window to appear visually (optional)
    else:
        print("Failed to open Microsoft Teams.")