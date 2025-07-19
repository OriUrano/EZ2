<script lang="ts">
	import { onMount } from 'svelte';

	interface Tag {
		Key: string;
		Value: string;
	}

	interface Instance {
		instanceId: string;
		instanceType: string;
		state: string;
		publicIpAddress?: string;
		privateIpAddress?: string;
		availabilityZone?: string;
		launchTime?: string;
		tags: Tag[];
	}

	let instances = $state<Instance[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let apiUrl = $state('');

	const statusColors = {
		running: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
		stopped: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
		pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
		stopping: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
		terminated: 'bg-neutral-100 text-neutral-800 dark:bg-neutral-700 dark:text-neutral-200'
	};

	async function fetchInstances() {
		if (!apiUrl) {
			error = 'Please set your Lambda Function URL';
			loading = false;
			return;
		}

		try {
			loading = true;
			error = null;
			
			const response = await fetch(apiUrl);
			
			if (!response.ok) {
				throw new Error(`HTTP ${response.status}: ${response.statusText}`);
			}
			
			const data = await response.json();
			instances = data.instances || [];
		} catch (err) {
			error = err instanceof Error ? err.message : 'An error occurred';
			instances = [];
		} finally {
			loading = false;
		}
	}

	function getTagValue(tags: Tag[], key: string): string {
		const tag = tags.find(t => t.Key === key);
		return tag ? tag.Value : '-';
	}

	function formatDate(dateString?: string): string {
		if (!dateString) return '-';
		return new Date(dateString).toLocaleString();
	}

	onMount(() => {
		const savedUrl = localStorage.getItem('lambdaFunctionUrl');
		if (savedUrl) {
			apiUrl = savedUrl;
			fetchInstances();
		} else {
			loading = false;
		}

		// Listen for settings updates
		const handleSettingsUpdate = () => {
			const savedUrl = localStorage.getItem('lambdaFunctionUrl');
			if (savedUrl) {
				apiUrl = savedUrl;
				fetchInstances();
			}
		};

		// Listen for refresh requests
		const handleRefreshRequest = () => {
			fetchInstances();
		};

		window.addEventListener('settingsUpdated', handleSettingsUpdate);
		window.addEventListener('refreshRequested', handleRefreshRequest);
		
		return () => {
			window.removeEventListener('settingsUpdated', handleSettingsUpdate);
			window.removeEventListener('refreshRequested', handleRefreshRequest);
		};
	});

</script>

<svelte:head>
	<title>EZ2 Dashboard</title>
</svelte:head>

<div class="bg-neutral-50 dark:bg-neutral-950 p-6 min-h-[94.15vh]">
	<div class="mx-auto max-w-7xl">

		<!-- Error Display -->
		{#if error}
			<div class="mb-6 rounded-lg bg-red-50 dark:bg-red-900/20 p-4 border border-red-200 dark:border-red-800">
				<div class="flex">
					<div class="flex-shrink-0">
						<svg class="h-5 w-5 text-red-400 dark:text-red-300" viewBox="0 0 20 20" fill="currentColor">
							<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
						</svg>
					</div>
					<div class="ml-3">
						<h3 class="text-sm font-medium text-red-800 dark:text-red-200">Error</h3>
						<div class="mt-1 text-sm text-red-700 dark:text-red-300">{error}</div>
					</div>
				</div>
			</div>
		{/if}

		<!-- Loading State -->
		{#if loading}
			<div class="flex justify-center items-center py-12">
				<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
				<span class="ml-3 text-neutral-600 dark:text-neutral-400">Loading instances...</span>
			</div>
		{:else if instances.length === 0 && !error}
			<div class="text-center py-12">
				<svg class="mx-auto h-12 w-12 text-neutral-400 dark:text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
				</svg>
				<h3 class="mt-4 text-lg font-medium text-neutral-900 dark:text-white">No instances found</h3>
				<p class="mt-2 text-neutral-500 dark:text-neutral-400">No EC2 instances are currently available.</p>
			</div>
		{:else}
			<!-- Instances Summary -->
			<div class="mb-6 grid grid-cols-1 gap-5 sm:grid-cols-3">
				<div class="bg-white dark:bg-neutral-800 overflow-hidden shadow dark:shadow-neutral-700 rounded-lg">
					<div class="p-5">
						<div class="flex items-center">
							<div class="flex-shrink-0">
								<svg class="h-6 w-6 text-neutral-400 dark:text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
								</svg>
							</div>
							<div class="ml-5 w-0 flex-1">
								<dl>
									<dt class="text-sm font-medium text-neutral-500 dark:text-neutral-400 truncate">Total Instances</dt>
									<dd class="text-lg font-medium text-neutral-900 dark:text-white">{instances.length}</dd>
								</dl>
							</div>
						</div>
					</div>
				</div>

				<div class="bg-white dark:bg-neutral-800 overflow-hidden shadow dark:shadow-neutral-700 rounded-lg">
					<div class="p-5">
						<div class="flex items-center">
							<div class="flex-shrink-0">
								<svg class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
							<div class="ml-5 w-0 flex-1">
								<dl>
									<dt class="text-sm font-medium text-neutral-500 dark:text-neutral-400 truncate">Running</dt>
									<dd class="text-lg font-medium text-neutral-900 dark:text-white">{instances.filter(i => i.state === 'running').length}</dd>
								</dl>
							</div>
						</div>
					</div>
				</div>

				<div class="bg-white dark:bg-neutral-800 overflow-hidden shadow dark:shadow-neutral-700 rounded-lg">
					<div class="p-5">
						<div class="flex items-center">
							<div class="flex-shrink-0">
								<svg class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
							<div class="ml-5 w-0 flex-1">
								<dl>
									<dt class="text-sm font-medium text-neutral-500 dark:text-neutral-400 truncate">Stopped</dt>
									<dd class="text-lg font-medium text-neutral-900 dark:text-white">{instances.filter(i => i.state === 'stopped').length}</dd>
								</dl>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Instances Table -->
			<div class="bg-white dark:bg-neutral-800 shadow dark:shadow-neutral-700 rounded-lg overflow-hidden">
				<div class="px-6 py-4 border-b border-neutral-200 dark:border-neutral-600">
					<h3 class="text-lg font-medium text-neutral-900 dark:text-white">EC2 Instances</h3>
				</div>
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-neutral-200 dark:divide-neutral-600">
						<thead class="bg-neutral-50 dark:bg-neutral-700">
							<tr>
								<th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-300 uppercase tracking-wider">Instance</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-300 uppercase tracking-wider">Name</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-300 uppercase tracking-wider">Type</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-300 uppercase tracking-wider">State</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-300 uppercase tracking-wider">IP Addresses</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-300 uppercase tracking-wider">Availability Zone</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-300 uppercase tracking-wider">Launch Time</th>
							</tr>
						</thead>
						<tbody class="bg-white dark:bg-neutral-800 divide-y divide-neutral-200 dark:divide-neutral-600">
							{#each instances as instance}
								<tr class="hover:bg-neutral-50 dark:hover:bg-neutral-700">
									<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-white">
										{instance.instanceId}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-300">
										{getTagValue(instance.tags, 'Name')}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-300">
										{instance.instanceType}
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full {statusColors[instance.state as keyof typeof statusColors] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'}">
											{instance.state}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-300">
										<div>
											{#if instance.publicIpAddress}
												<div>Public: {instance.publicIpAddress}</div>
											{/if}
											{#if instance.privateIpAddress}
												<div>Private: {instance.privateIpAddress}</div>
											{/if}
											{#if !instance.publicIpAddress && !instance.privateIpAddress}
												<span class="text-neutral-400 dark:text-neutral-500">-</span>
											{/if}
										</div>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-300">
										{instance.availabilityZone || '-'}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-300">
										{formatDate(instance.launchTime)}
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/if}
	</div>
</div>