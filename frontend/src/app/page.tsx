import { ChatInterface } from './components/ChatInterface';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-background to-background/80">
      <div className="w-full max-w-5xl">
        <ChatInterface />
      </div>
    </main>
  );
} 