<script lang="ts">
	import { X } from 'lucide-svelte';

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
		<div class="bg-white rounded-lg shadow-xl max-w-md w-full">
			<!-- Modal header -->
			<div class="flex items-center justify-between p-6 border-b border-gray-200">
				<h2 id="modal-title" class="text-lg font-semibold text-gray-900">Settings</h2>
				<button 
					onclick={closeModal}
					class="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md transition-colors"
				>
					<X size={20} />
				</button>
			</div>

			<!-- Modal body -->
			<div class="p-6">
				<div class="mb-4">
					<label for="apiUrl" class="block text-sm font-medium text-gray-700 mb-2">
						Lambda Function URL
					</label>
					<input
						id="apiUrl"
						type="url"
						bind:value={apiUrl}
						placeholder="https://your-lambda-function-url.lambda-url.region.on.aws/"
						class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
					/>
					<p class="mt-1 text-xs text-gray-500">
						Enter your AWS Lambda Function URL to fetch EC2 instance data
					</p>
				</div>
			</div>

			<!-- Modal footer -->
			<div class="flex justify-end gap-3 p-6 border-t border-gray-200">
				<button
					onclick={closeModal}
					class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
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