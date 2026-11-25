// Native Web Audio Synthesizer for Zero-Asset Meme Sounds

class SoundEngine {
  constructor() {
    this.ctx = null
    this.muted = false
  }

  init() {
    if (!this.ctx && typeof window !== 'undefined') {
      const AudioContext = window.AudioContext || window.webkitAudioContext
      if (AudioContext) {
        this.ctx = new AudioContext()
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume()
    }
  }

  toggleMute() {
    this.muted = !this.muted
    return this.muted
  }

  // Iconic Sub-bass Vine Boom effect
  playVineBoom() {
    if (this.muted) return
    this.init()
    if (!this.ctx) return

    const t = this.ctx.currentTime
    const osc = this.ctx.createOscillator()
    const gain = this.ctx.createGain()

    osc.type = 'sine'
    // Pitch drop from 130Hz to 30Hz
    osc.frequency.setValueAtTime(140, t)
    osc.frequency.exponentialRampToValueAtTime(32, t + 0.6)

    // Distortion / Punch envelope
    gain.gain.setValueAtTime(0.8, t)
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.9)

    osc.connect(gain)
    gain.connect(this.ctx.destination)

    osc.start(t)
    osc.stop(t + 0.9)
  }

  // 8-bit Victory / Absolute Cinema Fanfare
  playVictory() {
    if (this.muted) return
    this.init()
    if (!this.ctx) return

    const notes = [523.25, 659.25, 783.99, 1046.50] // C5, E5, G5, C6
    notes.forEach((freq, idx) => {
      const t = this.ctx.currentTime + idx * 0.1
      const osc = this.ctx.createOscillator()
      const gain = this.ctx.createGain()

      osc.type = 'triangle'
      osc.frequency.setValueAtTime(freq, t)

      gain.gain.setValueAtTime(0.3, t)
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.35)

      osc.connect(gain)
      gain.connect(this.ctx.destination)

      osc.start(t)
      osc.stop(t + 0.35)
    })
  }

  // Deadpan "Bruh" / Neutral Buzzer
  playBruh() {
    if (this.muted) return
    this.init()
    if (!this.ctx) return

    const t = this.ctx.currentTime
    const osc = this.ctx.createOscillator()
    const gain = this.ctx.createGain()

    osc.type = 'sawtooth'
    osc.frequency.setValueAtTime(110, t)
    osc.frequency.linearRampToValueAtTime(95, t + 0.4)

    gain.gain.setValueAtTime(0.25, t)
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.4)

    osc.connect(gain)
    gain.connect(this.ctx.destination)

    osc.start(t)
    osc.stop(t + 0.4)
  }
}

export const sounds = new SoundEngine()

