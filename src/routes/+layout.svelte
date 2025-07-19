<script lang="ts">
	import '../app.css';
	import { Settings } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import SettingsModal from '$lib/SettingsModal.svelte';

	let { children } = $props();
	let showSettingsModal = $state(false);
	let apiUrl = $state('');

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

<nav class="bg-white shadow">
	<div class="mx-auto max-w-7xl px-6">
		<div class="flex justify-between h-16">
			<div class="flex items-center">
				<a href="/" class="text-3xl font-bold text-gray-900">EZ2</a>
			</div>
			<div class="flex items-center gap-2">
				<button 
					onclick={() => window.dispatchEvent(new CustomEvent('refreshRequested'))}
					class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
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
					class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
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
