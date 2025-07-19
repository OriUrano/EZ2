<script lang="ts">
	import { X, Moon, Sun } from 'lucide-svelte';
	import { theme } from './stores/theme.js';

	let { isOpen = $bindable(), apiUrl = $bindable() } = $props();

	function closeModal() {
		isOpen = false;
	}

	function saveApiUrl() {
		localStorage.setItem('lambdaFunctionUrl', apiUrl);
		closeModal();
		// Dispatch custom event to trigger refresh
		window.dispatchEvent(new CustomEvent('settingsUpdated'));
	}

	function handleBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			closeModal();
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			closeModal();
		}
	}
</script>

{#if isOpen}
	<!-- Modal backdrop -->
	<div 
		class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
		onclick={handleBackdropClick}
		onkeydown={handleKeydown}
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
		tabindex="-1"
	>
		<!-- Modal content -->
		<div class="bg-white dark:bg-neutral-800 rounded-lg shadow-xl max-w-md w-full">
			<!-- Modal header -->
			<div class="flex items-center justify-between p-6 border-b border-neutral-200 dark:border-neutral-600">
				<h2 id="modal-title" class="text-lg font-semibold text-neutral-900 dark:text-white">Settings</h2>
				<button 
					onclick={closeModal}
					class="p-1 text-neutral-400 hover:text-neutral-600 hover:bg-neutral-100 dark:hover:bg-neutral-700 dark:hover:text-neutral-300 rounded-md transition-colors"
				>
					<X size={20} />
				</button>
			</div>

			<!-- Modal body -->
			<div class="p-6">
				<div class="mb-6">
					<label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-3">
						Appearance
					</label>
					<div class="flex items-center justify-between">
						<span class="text-sm text-gray-600 dark:text-gray-400">Dark mode</span>
						<button
							onclick={theme.toggle}
							class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 {$theme ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-600'}"
							role="switch"
							aria-checked={$theme ? 'true' : 'false'}
						>
							<span class="sr-only">Toggle dark mode</span>
							<span
								class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform {$theme ? 'translate-x-6' : 'translate-x-1'}"
							>
								{#if $theme}
									<Moon size={12} class="p-0.5 text-gray-600" />
								{:else}
									<Sun size={12} class="p-0.5 text-yellow-500" />
								{/if}
							</span>
						</button>
					</div>
				</div>

				<div class="mb-4">
					<label for="apiUrl" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
						Lambda Function URL
					</label>
					<input
						id="apiUrl"
						type="url"
						bind:value={apiUrl}
						placeholder="https://your-lambda-function-url.lambda-url.region.on.aws/"
						class="w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
					/>
					<p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
						Enter your AWS Lambda Function URL to fetch EC2 instance data
					</p>
				</div>
			</div>

			<!-- Modal footer -->
			<div class="flex justify-end gap-3 p-6 border-t border-gray-200 dark:border-gray-600">
				<button
					onclick={closeModal}
					class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
				>
					Cancel
				</button>
				<button
					onclick={saveApiUrl}
					class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
				>
					Save
				</button>
			</div>
		</div>
	</div>
{/if}