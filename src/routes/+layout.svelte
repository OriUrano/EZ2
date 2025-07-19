<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<nav class="bg-white shadow">
	<div class="mx-auto max-w-7xl px-6">
		<div class="flex justify-between h-16">
			<div class="flex items-center">
				<a href="/" class="text-xl font-bold text-gray-900">EZ2</a>
			</div>
		</div>
	</div>
</nav>

<main>
	{@render children()}
</main>
