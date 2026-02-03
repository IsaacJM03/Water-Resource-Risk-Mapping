const WS_URL = "ws://127.0.0.1:8000/ws/risk";

type MessageHandler = (data: any) => void;

let socket: WebSocket | null = null;

export function connectRealtime(onMessage: MessageHandler) {
  socket = new WebSocket(WS_URL);

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  socket.onerror = (err) => {
    console.error("WS error", err);
  };
}

export function disconnectRealtime() {
  socket?.close();
}
