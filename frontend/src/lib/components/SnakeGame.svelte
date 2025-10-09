<script>
	import { onMount, onDestroy } from 'svelte';

	const GRID_SIZE = 20;
	const GAME_SPEED = 150;

	let snake = [{ x: 10, y: 10 }];
	let food = getRandomFoodPosition();
	let direction = { x: 0, y: -1 };
	let score = 0;
	let isGameOver = false;
	let gameInterval;

	function getRandomFoodPosition() {
		let newFoodPosition;
		do {
			newFoodPosition = {
				x: Math.floor(Math.random() * GRID_SIZE),
				y: Math.floor(Math.random() * GRID_SIZE)
			};
		} while (isPositionOnSnake(newFoodPosition));
		return newFoodPosition;
	}

	function isPositionOnSnake(position) {
		return snake.some((segment) => segment.x === position.x && segment.y === position.y);
	}

	function updateGame() {
		if (isGameOver) return;

		const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };

		if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE || isPositionOnSnake(head)) {
			isGameOver = true;
			return;
		}

		snake.unshift(head);

		if (head.x === food.x && head.y === food.y) {
			score += 10;
			food = getRandomFoodPosition();
		} else {
			snake.pop();
		}
        		snake = snake;
	}

	function handleKeydown(e) {
		if (isGameOver) return;
		switch (e.key) {
			case 'ArrowUp': if (direction.y === 0) direction = { x: 0, y: -1 }; break;
			case 'ArrowDown': if (direction.y === 0) direction = { x: 0, y: 1 }; break;
			case 'ArrowLeft': if (direction.x === 0) direction = { x: -1, y: 0 }; break;
			case 'ArrowRight': if (direction.x === 0) direction = { x: 1, y: 0 }; break;
		}
	}

	function restartGame() {
		snake = [{ x: 10, y: 10 }];
		food = getRandomFoodPosition();
		direction = { x: 0, y: -1 };
		score = 0;
		isGameOver = false;
        
        snake = snake;
	}

	onMount(() => {
		gameInterval = setInterval(updateGame, GAME_SPEED);
	});

	onDestroy(() => {
		clearInterval(gameInterval);
	});
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center">
	<div class="bg-gray-800 p-4 rounded-lg shadow-2xl border border-gray-700">
		<h2 class="text-center text-2xl font-bold text-indigo-400 mb-4">Svelte Snake!</h2>

		<div
			class="relative bg-gray-900"
			style="width: {GRID_SIZE * 20}px; height: {GRID_SIZE * 20}px; display: grid; grid-template-columns: repeat({GRID_SIZE}, 1fr);"
		>
			{#each snake as segment, i}
				<div
					class="absolute {i === 0 ? 'bg-green-400' : 'bg-green-600'}"
					style="width: 20px; height: 20px; left: {segment.x * 20}px; top: {segment.y * 20}px;"
				></div>
			{/each}

			<div
				class="absolute bg-red-500 rounded-full"
				style="width: 20px; height: 20px; left: {food.x * 20}px; top: {food.y * 20}px;"
			></div>
		</div>

		<div class="mt-4 text-white text-center">
			{#if isGameOver}
				<div class="text-black-500 font-bold text-2xl">GAME OVER</div>
				<p>Punteggio: {score}</p>
				<button on:click={restartGame} class="mt-2 bg-indigo-600 px-4 py-2 rounded-lg">Rigioca</button>
			{:else}
				<p>Punteggio: {score}</p>
			{/if}
		</div>
	</div>
</div>