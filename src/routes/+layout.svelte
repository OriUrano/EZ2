<script lang="ts">
	import '../app.css';
	import { Settings } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import SettingsModal from '$lib/SettingsModal.svelte';
	import { theme } from '$lib/stores/theme.js';

	let { children } = $props();
	let showSettingsModal = $state(false);
	let apiUrl = $state('');
	
	// Subscribe to theme to ensure reactivity
	$effect(() => {
		$theme; // This ensures the theme store is subscribed to
	});

	onMount(() => {
		const savedUrl = localStorage.getItem('lambdaFunctionUrl');
		if (savedUrl) {
			apiUrl = savedUrl;
		}
	});

	function openSettings() {
		showSettingsModal = true;
	}
</script>

<nav class="bg-white dark:bg-neutral-950 shadow dark:shadow-neutral-900">
	<div class="mx-auto max-w-7xl px-6">
		<div class="flex justify-between h-16">
			<div class="flex items-center">
				<a href="/" class="text-3xl font-bold text-neutral-900 dark:text-white">EZ2</a>
			</div>
			<div class="flex items-center gap-2">
				<button 
					onclick={() => window.dispatchEvent(new CustomEvent('refreshRequested'))}
					class="p-2 text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-900 rounded-lg transition-colors"
					title="Refresh"
					aria-label="Refresh data"
				>
					<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
						<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
						<path d="M21 3v5h-5"/>
						<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
						<path d="M3 21v-5h5"/>
					</svg>
				</button>
				<button 
					onclick={openSettings}
					class="p-2 text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-900 rounded-lg transition-colors"
					title="Settings"
					aria-label="Open settings"
				>
					<Settings size={20} />
				</button>
			</div>
		</div>
	</div>
</nav>

<main>
	{@render children()}
</main>

<SettingsModal bind:isOpen={showSettingsModal} bind:apiUrl={apiUrl} />
