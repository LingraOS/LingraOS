export class DBClient {
  constructor(public url: string) {}

  connect() {
    console.log('Simulated DB connect to', this.url);
  }

  disconnect() {
    console.log('Simulated DB disconnect');
  }
}