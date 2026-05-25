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

  const wsRef = useRef<WebSocket | null>(null)
  const reconnectRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const attemptRef = useRef(0)
  const unmountedRef = useRef(false)

  useEffect(() => {
    unmountedRef.current = false
    attemptRef.current = 0

    function connect() {
      if (unmountedRef.current) return

      setStatus('connecting')
      const encodedPair = pair.replace('/', '-')
      const ws = new WebSocket(`${WS_BASE}/ws/prices/${encodedPair}`)
      wsRef.current = ws

      ws.onopen = () => {
        if (unmountedRef.current) { ws.close(); return }
        attemptRef.current = 0
        setStatus('live')
      }

      ws.onmessage = (evt: MessageEvent) => {
        if (unmountedRef.current) return
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
        if (unmountedRef.current) return
        setStatus('closed')
        scheduleReconnect()
      }

      ws.onerror = () => {
        if (unmountedRef.current) return
        setStatus('error')
        ws.close()
      }
    }

    function scheduleReconnect() {
      if (unmountedRef.current) return
      const delay = Math.min(1000 * 2 ** attemptRef.current, MAX_BACKOFF_MS)
      attemptRef.current += 1
      reconnectRef.current = setTimeout(connect, delay)
    }

    connect()

    return () => {
      unmountedRef.current = true
      if (reconnectRef.current !== null) clearTimeout(reconnectRef.current)
      wsRef.current?.close()
    }
  }, [pair])

  return { price, status }
}
