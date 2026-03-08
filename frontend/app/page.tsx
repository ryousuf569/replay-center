"use client";

import { useState } from "react";

export default function Home() {
  const [player, setPlayer] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const getRandomPlayer = async () => {
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/player_names/all");
      const data = await response.json();

      const players: string[] = data.players;

      if (players && players.length > 0) {
        const randomIndex = Math.floor(Math.random() * players.length);
        setPlayer(players[randomIndex]);
      } else {
        setPlayer("No players found.");
      }
    } catch (error) {
      setPlayer("Failed to fetch players.");
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-100">
      <main className="flex flex-col items-center gap-6 rounded-2xl bg-white p-10 shadow-lg">
        <h1 className="text-3xl font-bold text-black">Random NBA Player</h1>

        <button
          onClick={getRandomPlayer}
          disabled={loading}
          className="rounded-full bg-black px-6 py-3 text-white transition hover:bg-zinc-800 disabled:opacity-50"
        >
          {loading ? "Loading..." : "Get Random Player"}
        </button>

        {player && (
          <p className="text-xl font-medium text-zinc-700">{player}</p>
        )}
      </main>
    </div>
  );
}