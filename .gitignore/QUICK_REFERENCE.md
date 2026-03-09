# Space Fighters - Quick Reference Card

## Controls
| Action | Keys |
|--------|------|
| Move | WASD / Arrow Keys |
| Shoot | Space / Left Click |
| Drag Ship | Right Click + Drag |
| Pause | ESC / P |
| Menu Select | Enter / Space |
| Menu Navigate | Arrow Keys |

## Ships
| Ship | Unlock | Sound | Special |
|------|--------|-------|---------|
| Ship 1 | Default | ship_shoot.wav | Standard |
| Ship 2 | Level 2 | player_shoot.wav | Standard |
| Blue Ship | Level 4 | laser_shooting.wav | 20% faster fire |

## Bullet Levels
| Level | Pattern | Damage |
|-------|---------|--------|
| 1 | Single | 1 |
| 2 | Double | 2 |
| 3 | Triple Spread | 3 |
| 4 | Quad | 4 |

## Power-Ups
| Color | Effect |
|-------|--------|
| Yellow | +1 Bullet Level |
| Red | +30 HP |
| Green | Shield + 20 HP |

## Levels
| Level | Enemies | Boss | Planet |
|-------|---------|------|--------|
| 1 | enemy_L1 | boss_L1 | planet-1 |
| 2 | enemy_L2 | boss_L2 | planet-2 |
| 3 | enemy_L3 | boss_L3 | planet-3 |
| 4 | enemy_L4 | boss_L4 | planet-4 |
| 5 | enemy_L5 | boss_L5_ship | planet-5 |
| Bonus | Asteroids | None | Bonus BG |

## Damage Values
| Source | Damage |
|--------|--------|
| Enemy Bullet | 10 |
| Enemy Collision | 20 |
| Asteroid | 15 |

## Scoring
| Action | Points |
|--------|--------|
| Enemy Kill | 10 × Level |
| Boss Kill | 500 |
| Power-Up | 50 |
| Asteroid | 20 |

## Time Limits
| Mission | Time |
|---------|------|
| Regular Level | 90s |
| Bonus Mission | 60s |

## Sound Effects
| Event | Sound |
|-------|-------|
| Ship 1 Shoot | ship_shoot.wav |
| Ship 2 Shoot | player_shoot.wav |
| Blue Ship Shoot | laser_shooting.wav |
| Enemy Death | explosion_1.wav |
| Boss Death | explosion_2.wav |
| Level Complete | mission_complete.wav |
| Final Victory | Win.mp3 |
| Game Over | game_over.wav → loose.wav |
| Background | background_sound.wav |

## Settings Menu
| Option | Control |
|--------|---------|
| Music Volume | LEFT/RIGHT (0-100%) |
| Sound Volume | LEFT/RIGHT (0-100%) |
| Mute Music | ENTER (Toggle) |
| Mute Sounds | ENTER (Toggle) |
| Reset Game | ENTER (Confirm with Y) |

## Progression
1. Start → Level 1
2. Complete L1 → Unlock Ship 2, Level 2
3. Complete L2 → Unlock Level 3
4. Complete L3 → Unlock Level 4
5. Complete L4 → Unlock Blue Ship, Bonus Mission, Level 5
6. Bonus Mission → Gain power-ups
7. Complete L5 → Victory!

## Tips
- ✓ Collect power-ups to increase bullet level
- ✓ Bullet level decreases when hit
- ✓ Do bonus mission before Level 5
- ✓ Shield protects bullet level
- ✓ Stay mobile to avoid bullets
- ✓ Progress saves automatically

## File Locations
| Type | Path |
|------|------|
| Player Images | assets/images/player/ |
| Enemy Images | assets/images/enemy/ |
| Level Images | assets/images/levels/ |
| Sounds | assets/sounds/ |
| Save File | game_save.json |

## Troubleshooting
| Issue | Solution |
|-------|----------|
| No sound | Check Settings → Unmute |
| No graphics | Check assets/images/ folder |
| Won't save | Check write permissions |
| Slow performance | Reduce window size |

---
**Version**: Enhanced Edition
**Python**: 3.7+
**Pygame**: 2.0+
