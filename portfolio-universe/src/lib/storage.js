const DATA_KEY = 'elsewhere:portfolio:v1'
const PREFS_KEY = 'elsewhere:preferences:v1'

export function readStored(key, fallback) {
  try {
    const saved = localStorage.getItem(key)
    return saved ? JSON.parse(saved) : fallback
  } catch {
    return fallback
  }
}

export function savePortfolio(value) { localStorage.setItem(DATA_KEY, JSON.stringify(value)) }
export function savePreferences(value) { localStorage.setItem(PREFS_KEY, JSON.stringify(value)) }
export function portfolioKey() { return DATA_KEY }
