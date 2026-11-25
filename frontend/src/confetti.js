// Canvas Confetti Burst for Absolute Cinema W-Moments

export function triggerConfetti() {
  const canvas = document.createElement('canvas')
  canvas.style.position = 'fixed'
  canvas.style.top = '0'
  canvas.style.left = '0'
  canvas.style.width = '100vw'
  canvas.style.height = '100vh'
  canvas.style.pointerEvents = 'none'
  canvas.style.zIndex = '99999'
  document.body.appendChild(canvas)

  const ctx = canvas.getContext('2d')
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight

  const colors = ['#f43f5e', '#38bdf8', '#10b981', '#fbbf24', '#c084fc', '#ffffff']
  const particles = Array.from({ length: 90 }, () => ({
    x: canvas.width / 2,
    y: canvas.height / 2,
    vx: (Math.random() - 0.5) * 16,
    vy: (Math.random() - 0.8) * 18,
    size: Math.random() * 8 + 4,
    color: colors[Math.floor(Math.random() * colors.length)],
    rotation: Math.random() * 360,
    vr: (Math.random() - 0.5) * 12,
    alpha: 1
  }))

  let frame = 0
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    let active = false

    particles.forEach((p) => {
      p.x += p.vx
      p.y += p.vy
      p.vy += 0.35 // Gravity
      p.rotation += p.vr
      p.alpha -= 0.012

      if (p.alpha > 0) {
        active = true
        ctx.save()
        ctx.translate(p.x, p.y)
        ctx.rotate((p.rotation * Math.PI) / 180)
        ctx.fillStyle = p.color
        ctx.globalAlpha = Math.max(0, p.alpha)
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6)
        ctx.restore()
      }
    })

    frame++
    if (active && frame < 120) {
      requestAnimationFrame(animate)
    } else {
      document.body.removeChild(canvas)
    }
  }

  requestAnimationFrame(animate)
}

