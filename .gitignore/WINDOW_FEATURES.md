# Space Fighters - Window Management Features

## Full Window Support

Space Fighters now fully supports all standard window operations on Windows!

---

## Supported Window Operations

### 1. **Resize Window**
- **Drag window edges** to resize
- **Drag corners** for proportional resize
- Game automatically scales to fit new window size
- Background images scale smoothly
- HUD elements reposition appropriately
- Player stays within new bounds

### 2. **Minimize Window**
- Click the **minimize button** (—) in title bar
- Or press **Windows + Down Arrow**
- Game continues running in background
- Window can be restored from taskbar

### 3. **Maximize Window**
- Click the **maximize button** (□) in title bar
- Or press **Windows + Up Arrow**
- Or double-click title bar
- Game fills entire screen
- All elements scale to full screen size

### 4. **Restore Window**
- Click the **restore button** (⧉) when maximized
- Or press **Windows + Down Arrow** when maximized
- Or double-click title bar when maximized
- Returns to previous window size

### 5. **Close Window**
- Click the **close button** (✕) in title bar
- Or press **Alt + F4**
- Or click the X button
- Game exits cleanly

---

## Window Behavior

### Automatic Scaling
- **Background**: Scales to fill window while maintaining aspect ratio
- **Sprites**: Maintain their size (for gameplay consistency)
- **HUD Elements**: Reposition based on window size
  - Health bar: Bottom-left corner
  - Time: Top-right corner
  - Score/Level: Top-left corner
  - Boss health: Centered at top

### Bounds Management
- Player ship automatically stays within window bounds
- When window is resized, player position adjusts if needed
- Enemies and bullets respect new window dimensions

### Performance
- Smooth scaling with no lag
- Background is rescaled only when window size changes
- Efficient rendering at any window size

---

## Keyboard Shortcuts

### Windows Standard Shortcuts:
- **Alt + F4**: Close window
- **Windows + Up Arrow**: Maximize window
- **Windows + Down Arrow**: Minimize/Restore window
- **Alt + Space**: Open window menu

### In-Game Shortcuts:
- **ESC**: (Can be added) Pause game
- **F11**: (Can be added) Toggle fullscreen

---

## Technical Details

### Window Modes Supported:
- **Windowed Mode**: Default, resizable
- **Maximized Mode**: Full screen with title bar
- **Minimized Mode**: Hidden in taskbar

### Window Events Handled:
- `VIDEORESIZE`: Window size changed
- `WINDOWEVENT_MINIMIZED`: Window minimized
- `WINDOWEVENT_RESTORED`: Window restored
- `WINDOWEVENT_MAXIMIZED`: Window maximized
- `WINDOWEVENT_FOCUS_LOST`: Window lost focus
- `WINDOWEVENT_FOCUS_GAINED`: Window gained focus
- `QUIT`: Window closed

### Scaling System:
- Maintains scale factors (scale_x, scale_y)
- Dynamically updates on resize
- Preserves gameplay area proportions
- Smooth transitions between sizes

---

## Tips for Best Experience

1. **Default Size**: Start with default 800x600 for optimal experience
2. **Maximize**: Use maximize for immersive full-screen gameplay
3. **Custom Size**: Resize to fit your screen preference
4. **Multi-Monitor**: Drag to any monitor and resize as needed
5. **Quick Switch**: Minimize to quickly switch to other apps

---

## Responsive Design Features

### Adaptive Layout:
- HUD elements reposition based on window size
- Health bar scales proportionally
- Boss health bar centers dynamically
- Text remains readable at all sizes

### Gameplay Consistency:
- Ship speed remains constant
- Bullet speed unchanged
- Enemy behavior consistent
- Collision detection accurate at any size

### Visual Quality:
- Background images scale smoothly
- No pixelation or distortion
- Maintains aspect ratio
- Clean rendering at all sizes

---

## Troubleshooting

### Window Too Small?
- Drag edges to make larger
- Or click maximize button
- Minimum recommended: 640x480

### Window Too Large?
- Click restore button
- Or drag edges to resize smaller
- Or minimize and restore

### Game Not Responding to Resize?
- Try closing and reopening
- Check if window is in focus
- Ensure you're dragging edges, not moving window

### Performance Issues?
- Smaller window = better performance
- Close other applications
- Update graphics drivers

---

## Future Enhancements

Potential additions:
- Fullscreen mode (F11)
- Custom resolution selector
- Aspect ratio lock option
- Window position memory
- Multi-monitor support improvements
- Borderless windowed mode

---

## Summary

Space Fighters fully supports:
✓ Window resizing (drag edges/corners)
✓ Minimize to taskbar
✓ Maximize to full screen
✓ Restore to previous size
✓ Close window (X button, Alt+F4)
✓ Automatic scaling and repositioning
✓ Smooth performance at any size
✓ All standard Windows window operations

**Play at any size you want - the game adapts to your window!**
