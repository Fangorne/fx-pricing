import { useEffect, useRef, useState } from 'react'
import type { SpotPrice, StreamStatus } from '@/types/fx'

const WS_BASE = (import.meta.env.VITE_WS_URL as string | undefined) ?? 'ws://localhost:8000'
const MAX_BACKOFF_MS = 30_000

interface UseSpotStreamResult {
  price: SpotPrice | null
  status: StreamStatus
}

export function useSpotStream(pair: string): UseSpotStreamResult {
  const [price, setPrice] = useState<SpotPrice | null>(null)
  const [status, setStatus] = useState<StreamStatus>('connecting')

  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    // Per-effect cancellation flag — not shared across pair changes.
    // A shared ref would be reset to false by the new effect before the old
    // WebSocket's onclose fires, causing the old connection to schedule a
    // reconnect for the stale pair.
    let cancelled = false
    let attempt = 0
    let ws: WebSocket | null = null

    function connect() {
      if (cancelled) return

      setStatus('connecting')
      const encodedPair = pair.replace('/', '-')
      ws = new WebSocket(`${WS_BASE}/ws/prices/${encodedPair}`)

      ws.onopen = () => {
        if (cancelled) { ws?.close(); return }
        attempt = 0
        setStatus('live')
      }

      ws.onmessage = (evt: MessageEvent) => {
        if (cancelled) return
        try {
          const data = JSON.parse(evt.data as string) as Record<string, unknown>
          if ('error' in data) {
            setStatus('error')
          } else {
            setPrice(data as unknown as SpotPrice)
            setStatus('live')
          }
        } catch {
          // ignore malformed frames
        }
      }

      ws.onclose = () => {
        if (cancelled) return
        setStatus('closed')
        const delay = Math.min(1000 * 2 ** attempt, MAX_BACKOFF_MS)
        attempt += 1
        reconnectTimerRef.current = setTimeout(connect, delay)
      }

      ws.onerror = () => {
        if (cancelled) return
        setStatus('error')
        ws?.close()
      }
    }

    connect()

    return () => {
      cancelled = true
      if (reconnectTimerRef.current !== null) {
        clearTimeout(reconnectTimerRef.current)
        reconnectTimerRef.current = null
      }
      ws?.close()
    }
  }, [pair])

  return { price, status }
}
