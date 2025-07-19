<script>
	import { onMount } from 'svelte';

	let instances = $state([]);
	let loading = $state(true);
	let error = $state(null);
	let apiUrl = $state('');

	const statusColors = {
		running: 'bg-green-100 text-green-800',
		stopped: 'bg-red-100 text-red-800',
		pending: 'bg-yellow-100 text-yellow-800',
		stopping: 'bg-orange-100 text-orange-800',
		terminated: 'bg-gray-100 text-gray-800'
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
			error = err.message;
			instances = [];
		} finally {
			loading = false;
		}
	}

	function getTagValue(tags, key) {
		const tag = tags.find(t => t.Key === key);
		return tag ? tag.Value : '-';
	}

	function formatDate(dateString) {
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
	});

	function saveApiUrl() {
		localStorage.setItem('lambdaFunctionUrl', apiUrl);
		fetchInstances();
	}
</script>

<svelte:head>
	<title>EC2 Dashboard</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 p-6">
	<div class="mx-auto max-w-7xl">
		<div class="mb-8">
			<h1 class="text-3xl font-bold text-gray-900">EC2 Dashboard</h1>
			<p class="mt-2 text-gray-600">Monitor and manage your AWS EC2 instances</p>
		</div>

		<!-- API URL Configuration -->
		<div class="mb-6 rounded-lg bg-white p-6 shadow">
			<h2 class="mb-4 text-lg font-semibold text-gray-900">Lambda Function URL</h2>
			<div class="flex gap-4">
				<input
					type="url"
					bind:value={apiUrl}
					placeholder="https://your-lambda-function-url.lambda-url.region.on.aws/"
					class="flex-1 rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
				/>
				<button
					onclick={saveApiUrl}
					class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
				>
					Save & Fetch
				</button>
				<button
					onclick={fetchInstances}
					disabled={!apiUrl || loading}
					class="rounded-md bg-gray-600 px-4 py-2 text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:opacity-50"
				>
					Refresh
				</button>
			</div>
		</div>

		<!-- Error Display -->
		{#if error}
			<div class="mb-6 rounded-lg bg-red-50 p-4 border border-red-200">
				<div class="flex">
					<div class="flex-shrink-0">
						<svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
							<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
						</svg>
					</div>
					<div class="ml-3">
						<h3 class="text-sm font-medium text-red-800">Error</h3>
						<div class="mt-1 text-sm text-red-700">{error}</div>
					</div>
				</div>
			</div>
		{/if}

		<!-- Loading State -->
		{#if loading}
			<div class="flex justify-center items-center py-12">
				<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
				<span class="ml-3 text-gray-600">Loading instances...</span>
			</div>
		{:else if instances.length === 0 && !error}
			<div class="text-center py-12">
				<svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
				</svg>
				<h3 class="mt-4 text-lg font-medium text-gray-900">No instances found</h3>
				<p class="mt-2 text-gray-500">No EC2 instances are currently available.</p>
			</div>
		{:else}
			<!-- Instances Summary -->
			<div class="mb-6 grid grid-cols-1 gap-5 sm:grid-cols-3">
				<div class="bg-white overflow-hidden shadow rounded-lg">
					<div class="p-5">
						<div class="flex items-center">
							<div class="flex-shrink-0">
								<svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
								</svg>
							</div>
							<div class="ml-5 w-0 flex-1">
								<dl>
									<dt class="text-sm font-medium text-gray-500 truncate">Total Instances</dt>
									<dd class="text-lg font-medium text-gray-900">{instances.length}</dd>
								</dl>
							</div>
						</div>
					</div>
				</div>

				<div class="bg-white overflow-hidden shadow rounded-lg">
					<div class="p-5">
						<div class="flex items-center">
							<div class="flex-shrink-0">
								<svg class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
							<div class="ml-5 w-0 flex-1">
								<dl>
									<dt class="text-sm font-medium text-gray-500 truncate">Running</dt>
									<dd class="text-lg font-medium text-gray-900">{instances.filter(i => i.state === 'running').length}</dd>
								</dl>
							</div>
						</div>
					</div>
				</div>

				<div class="bg-white overflow-hidden shadow rounded-lg">
					<div class="p-5">
						<div class="flex items-center">
							<div class="flex-shrink-0">
								<svg class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
							<div class="ml-5 w-0 flex-1">
								<dl>
									<dt class="text-sm font-medium text-gray-500 truncate">Stopped</dt>
									<dd class="text-lg font-medium text-gray-900">{instances.filter(i => i.state === 'stopped').length}</dd>
								</dl>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Instances Table -->
			<div class="bg-white shadow rounded-lg overflow-hidden">
				<div class="px-6 py-4 border-b border-gray-200">
					<h3 class="text-lg font-medium text-gray-900">EC2 Instances</h3>
				</div>
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Instance</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">State</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP Addresses</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Availability Zone</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Launch Time</th>
							</tr>
						</thead>
						<tbody class="bg-white divide-y divide-gray-200">
							{#each instances as instance}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
										{instance.instanceId}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										{getTagValue(instance.tags, 'Name')}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										{instance.instanceType}
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full {statusColors[instance.state] || 'bg-gray-100 text-gray-800'}">
											{instance.state}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										<div>
											{#if instance.publicIpAddress}
												<div>Public: {instance.publicIpAddress}</div>
											{/if}
											{#if instance.privateIpAddress}
												<div>Private: {instance.privateIpAddress}</div>
											{/if}
											{#if !instance.publicIpAddress && !instance.privateIpAddress}
												<span class="text-gray-400">-</span>
											{/if}
										</div>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										{instance.availabilityZone || '-'}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
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