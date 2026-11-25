import React, { useState, useEffect, useCallback, useMemo } from 'react'
import { sounds } from './soundEffects'
import { triggerConfetti } from './confetti'

// Fallback Canvas Image Generator
function createFallbackBlob(title, emoji, bgColors) {
  const canvas = document.createElement('canvas')
  canvas.width = 400
  canvas.height = 300
  const ctx = canvas.getContext('2d')

  const grad = ctx.createLinearGradient(0, 0, 400, 300)
  grad.addColorStop(0, bgColors?.[0] || '#e11d48')
  grad.addColorStop(1, bgColors?.[1] || '#4f46e5')
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, 400, 300)

  ctx.strokeStyle = '#000000'
  ctx.lineWidth = 10
  ctx.strokeRect(5, 5, 390, 290)

  ctx.font = '80px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(emoji || '🎭', 200, 150)

  ctx.font = 'bold 22px system-ui, sans-serif'
  ctx.fillStyle = '#ffffff'
  ctx.fillText(title, 200, 225)

  return new Promise((resolve) => {
    canvas.toBlob((blob) => {
      resolve(new File([blob], `${title.toLowerCase().replace(/\s+/g, '_')}.png`, { type: 'image/png' }))
    }, 'image/png')
  })
}

export default function App() {
  const [caption, setCaption] = useState('')
  const [imageFile, setImageFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [muted, setMuted] = useState(false)

  // 100% Unique Memes Gallery State
  const [memes, setMemes] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('All')

  // Split caption for the classic Top/Bottom Impact meme text
  const { topText, bottomText } = useMemo(() => {
    if (!caption.trim()) return { topText: '', bottomText: '' }
    const words = caption.trim().split(' ')
    if (words.length <= 4) return { topText: caption.trim(), bottomText: '' }
    const mid = Math.ceil(words.length / 2)
    return {
      topText: words.slice(0, mid).join(' '),
      bottomText: words.slice(mid).join(' ')
    }
  }, [caption])

  // Fetch unique non-repetitive memes from backend API
  const fetchMemes = useCallback(async (queryStr, lang) => {
    try {
      const params = new URLSearchParams({
        page: '1',
        limit: '100',
        query: queryStr,
        language: lang
      })
      const resp = await fetch(`/api/memes?${params.toString()}`)
      if (resp.ok) {
        const data = await resp.json()
        setMemes(data.memes)
      }
    } catch (err) {
      console.error('Failed to load memes:', err)
    }
  }, [])

  useEffect(() => {
    const handler = setTimeout(() => {
      fetchMemes(searchQuery, selectedLanguage)
    }, 150)
    return () => clearTimeout(handler)
  }, [searchQuery, selectedLanguage, fetchMemes])

  // Dynamic ambient glow based on classification
  useEffect(() => {
    if (!result) {
      document.documentElement.style.setProperty('--glow-color', 'rgba(168, 85, 247, 0.4)')
      return
    }
    if (result.predicted_sentiment === 'positive') {
      document.documentElement.style.setProperty('--glow-color', 'rgba(16, 185, 129, 0.5)')
    } else if (result.predicted_sentiment === 'negative') {
      document.documentElement.style.setProperty('--glow-color', 'rgba(244, 63, 94, 0.55)')
    } else {
      document.documentElement.style.setProperty('--glow-color', 'rgba(245, 158, 11, 0.45)')
    }
  }, [result])

  const toggleSound = () => {
    const isMuted = sounds.toggleMute()
    setMuted(isMuted)
  }

  const handleCustomUpload = (e) => {
    const file = e.target.files[0]
    if (!file) return

    if (file.size > 5 * 1024 * 1024) {
      setError('Meme file exceeds 5 MB.')
      return
    }

    setError('')
    setImageFile(file)
    setPreviewUrl(URL.createObjectURL(file))
  }

  const runPrediction = async (textToPredict, fileToPredict) => {
    setError('')
    setResult(null)
    setLoading(true)

    const formData = new FormData()
    formData.append('text', textToPredict)
    formData.append('image', fileToPredict)

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || 'Inference error.')
      }

      const data = await response.json()
      setResult(data)

      // Sound FX & Visual Flair trigger
      if (data.predicted_sentiment === 'positive') {
        sounds.playVictory()
        triggerConfetti()
      } else if (data.predicted_sentiment === 'negative') {
        sounds.playVineBoom()
      } else {
        sounds.playBruh()
      }
    } catch (err) {
      setError(err.message || 'Model unreachable.')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!caption.trim()) {
      setError('Type a caption or pick one below!')
      return
    }
    if (!imageFile) {
      setError('Select an image or hit Surprise Me!')
      return
    }
    runPrediction(caption.trim(), imageFile)
  }

  const handleCookMeme = async (meme) => {
    setCaption(meme.caption)
    window.scrollTo({ top: 0, behavior: 'smooth' })

    try {
      const resp = await fetch(meme.imageUrl).catch(() => null)
      let file
      if (resp && resp.ok) {
        const blob = await resp.blob()
        file = new File([blob], `${meme.id}.png`, { type: blob.type || 'image/png' })
      } else {
        file = await createFallbackBlob(meme.title, meme.emoji, meme.fallbackBg)
      }
      setImageFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      runPrediction(meme.caption, file)
    } catch {
      const file = await createFallbackBlob(meme.title, meme.emoji, meme.fallbackBg)
      setImageFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      runPrediction(meme.caption, file)
    }
  }

  // Random Meme Roulette
  const handleRandomMeme = () => {
    if (memes.length > 0) {
      const randomMeme = memes[Math.floor(Math.random() * memes.length)]
      handleCookMeme(randomMeme)
    }
  }

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text)
  }

  const handleDownload = async (meme) => {
    try {
      const resp = await fetch(meme.imageUrl).catch(() => null)
      let blobUrl
      if (resp && resp.ok) {
        const blob = await resp.blob()
        blobUrl = URL.createObjectURL(blob)
      } else {
        const file = await createFallbackBlob(meme.title, meme.emoji, meme.fallbackBg)
        blobUrl = URL.createObjectURL(file)
      }
      const a = document.createElement('a')
      a.href = blobUrl
      a.download = `${meme.title.toLowerCase().replace(/\s+/g, '_')}.png`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    } catch (e) {
      console.error(e)
    }
  }

  const getStamp = (sentiment, conf) => {
    switch (sentiment) {
      case 'positive':
        return {
          cardClass: 'stamp-positive',
          badgeText: `🔥 ${(conf * 100).toFixed(0)}% CERTIFIED CINEMA`,
          badgeBg: '#10b981',
          title: 'W RIZZ / PURE PEAK',
          desc: 'Brahmanandam & Leo Approved. 10/10 masterwork.',
          color: 'var(--positive)'
        }
      case 'negative':
        return {
          cardClass: 'stamp-negative',
          badgeText: `💀 ${(conf * 100).toFixed(0)}% CERTIFIED CRINGE`,
          badgeBg: '#f43f5e',
          title: 'MASSIVE L / COOKED',
          desc: 'Vine boom moment. Emotional damage overload.',
          color: 'var(--negative)'
        }
      default:
        return {
          cardClass: 'stamp-neutral',
          badgeText: `🗿 50% CERTIFIED NPC`,
          badgeBg: '#f59e0b',
          title: 'UNBOTHERED / MID',
          desc: 'Zero thoughts, head empty. Perfectly balanced.',
          color: 'var(--neutral)'
        }
    }
  }

  const languages = ['All', 'Telugu', 'Bengali', 'Hindi', 'Tamil', 'Global']

  return (
    <div className="app-wrapper">
      {/* Top Strip */}
      <div className="top-strip">
        <div className="meme-badge-pill">
          ★ CERTIFIED DANK MEME AI ★
        </div>
        <button className="sound-toggle-btn" onClick={toggleSound}>
          {muted ? '🔇 Sound FX: OFF' : '🔊 Sound FX: ON'}
        </button>
      </div>

      {/* Hero Header */}
      <header className="hero">
        <h1>IndicSent-Meme Studio</h1>
        <p>Combining BERT multilingual NLP with ResNet cross-modal attention to review shitposts with unbothered precision.</p>
      </header>

      {/* Main Studio Grid */}
      <div className="studio-grid">
        {/* Left: Meme Canvas & Creator */}
        <div className="studio-panel">
          <div className="panel-header">
            <h2>🎨 Interactive Meme Canvas</h2>
            <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '700' }}>Live Impact Preview</span>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Live Meme Canvas */}
            <label className="meme-canvas-wrapper">
              <input
                type="file"
                accept="image/png, image/jpeg, image/webp"
                onChange={handleCustomUpload}
                style={{ display: 'none' }}
              />
              {previewUrl ? (
                <>
                  <img src={previewUrl} alt="Meme Canvas" />
                  {topText && <div className="meme-text-overlay meme-text-top">{topText}</div>}
                  {bottomText && <div className="meme-text-overlay meme-text-bottom">{bottomText}</div>}
                </>
              ) : (
                <div className="empty-canvas-cta">
                  <div style={{ fontSize: '38px', marginBottom: '4px' }}>🖼️</div>
                  <p style={{ fontWeight: '800', fontSize: '14px', textTransform: 'uppercase' }}>Tap to Load Image</p>
                  <p style={{ fontSize: '11px', color: '#64748b', marginTop: '2px' }}>or choose a viral meme below</p>
                </div>
              )}
            </label>

            <input
              type="text"
              className="caption-input"
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
              placeholder="Type your meme caption here..."
            />

            {error && <div style={{ color: '#f87171', fontSize: '12px', fontWeight: '700', marginBottom: '10px' }}>{error}</div>}

            <div className="btn-row">
              <button type="submit" className="btn-boom" disabled={loading}>
                {loading ? 'Cooking...' : '💥 VINE BOOM & COOK 💥'}
              </button>
              <button
                type="button"
                className="btn-roulette"
                onClick={handleRandomMeme}
              >
                🎲 Surprise Me
              </button>
            </div>
          </form>
        </div>

        {/* Right: Certified Review Stamp */}
        <div className="studio-panel" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <div className="panel-header">
            <h2>📊 Neural Vibe Review</h2>
            <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '700' }}>Rotten Memes™</span>
          </div>

          {result ? (
            <div>
              {(() => {
                const s = getStamp(result.predicted_sentiment, result.confidence)
                return (
                  <div className={`verdict-stamp-card ${s.cardClass}`}>
                    <div className="stamp-badge" style={{ background: s.badgeBg, color: '#000' }}>
                      {s.badgeText}
                    </div>
                    <div className="stamp-title" style={{ color: s.color }}>
                      {s.title}
                    </div>
                    <p className="stamp-desc">{s.desc}</p>
                    <div style={{ fontSize: '12px', color: '#94a3b8', fontWeight: '700' }}>
                      Neural Model Confidence: {(result.confidence * 100).toFixed(1)}%
                    </div>
                  </div>
                )
              })()}

              <div style={{ marginTop: '12px' }}>
                <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '800', letterSpacing: '0.5px' }}>
                  PROBABILITY BREAKDOWN
                </span>

                {Object.entries(result.class_probabilities).map(([key, val]) => {
                  let barColor = 'var(--neutral)'
                  let icon = '🗿'
                  if (key === 'positive') { barColor = 'var(--positive)'; icon = '🔥' }
                  if (key === 'negative') { barColor = 'var(--negative)'; icon = '💀' }

                  return (
                    <div key={key} className="prob-meter">
                      <div className="prob-meter-label">
                        <span style={{ textTransform: 'capitalize' }}>{icon} {key}</span>
                        <span>{(val * 100).toFixed(1)}%</span>
                      </div>
                      <div className="prob-track">
                        <div
                          className="prob-fill"
                          style={{
                            width: `${val * 100}%`,
                            backgroundColor: barColor
                          }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '40px 10px', color: '#475569' }}>
              <div style={{ fontSize: '48px', marginBottom: '8px' }}>🗿</div>
              <p style={{ fontWeight: '800', color: '#94a3b8', fontSize: '15px' }}>Waiting for a shitpost</p>
              <p style={{ fontSize: '12px', marginTop: '4px' }}>
                Load an image, type a dialogue, or hit Surprise Me!
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Toolbar: Search & Language Filter */}
      <div className="gallery-toolbar">
        <input
          type="text"
          className="search-field"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search unique dialogues, characters, or movies..."
        />
        <div className="filter-pills">
          {languages.map((lang) => (
            <button
              key={lang}
              className={`filter-pill ${selectedLanguage === lang ? 'filter-pill-active' : ''}`}
              onClick={() => setSelectedLanguage(lang)}
            >
              {lang}
            </button>
          ))}
        </div>
      </div>

      {/* 100% Unique Meme Gallery */}
      <div className="memes-grid">
        {memes.map((meme) => (
          <div key={meme.id} className="meme-card">
            <div className="meme-card-img-wrap">
              <img
                src={meme.imageUrl}
                alt={meme.title}
                loading="lazy"
                onError={(e) => {
                  e.target.style.display = 'none'
                  const p = e.target.parentNode
                  p.style.background = `linear-gradient(135deg, ${meme.fallbackBg?.[0] || '#e11d48'}, ${meme.fallbackBg?.[1] || '#4f46e5'})`
                  p.style.display = 'flex'
                  p.style.alignItems = 'center'
                  p.style.justifyContent = 'center'
                  p.style.fontSize = '44px'
                  p.innerText = meme.emoji || '🎭'
                }}
              />
              <span className="meme-sticker">{meme.tag}</span>
            </div>

            <div className="meme-card-content">
              <div>
                <h3 className="meme-card-title">{meme.title}</h3>
                <p className="meme-card-caption">"{meme.caption}"</p>
              </div>

              <div>
                <div className="card-action-bar">
                  <button
                    className="card-action-btn"
                    onClick={() => handleCopy(meme.caption)}
                    title="Copy caption"
                  >
                    📋 Copy
                  </button>
                  <button
                    className="card-action-btn"
                    onClick={() => handleDownload(meme)}
                    title="Save image"
                  >
                    📥 Save
                  </button>
                </div>

                <button
                  className="card-cook-btn"
                  onClick={() => handleCookMeme(meme)}
                >
                  ⚡ Cook in Studio
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
