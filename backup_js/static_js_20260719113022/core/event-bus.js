// Lightweight event bus
export class EventBus {
  constructor() {
    this.listeners = new Map();
  }

  on(event, callback) {
    if (!this.listeners.has(event)) this.listeners.set(event, []);
    this.listeners.get(event).push(callback);
  }

  emit(event, payload) {
    (this.listeners.get(event) || []).forEach((callback) => callback(payload));
  }
}
