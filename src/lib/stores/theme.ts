import { writable } from 'svelte/store';
import { browser } from '$app/environment';

declare global {
	interface Window {
		__themeListenerAdded?: boolean;
	}
}

function createThemeStore() {
	const { subscribe, set } = writable(false);

	function applyTheme() {
		if (!browser) return;
		
		// Use Tailwind's exact pattern but read current DOM state first
		const currentlyDark = document.documentElement.classList.contains('dark');
		const shouldBeDark = localStorage.theme === 'dark' || 
			(!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches);
		
		// Only manipulate DOM if there's an actual change needed
		if (currentlyDark !== shouldBeDark) {
			if (shouldBeDark) {
				document.documentElement.classList.add('dark');
			} else {
				document.documentElement.classList.remove('dark');
			}
		}
		
		set(shouldBeDark);
	}

	function toggle() {
		if (!browser) return;
		
		// Read current actual state from DOM to avoid race conditions
		const currentlyDark = document.documentElement.classList.contains('dark');
		const newTheme = currentlyDark ? 'light' : 'dark';
		
		localStorage.theme = newTheme;
		
		// Apply immediately and synchronously
		if (newTheme === 'dark') {
			document.documentElement.classList.add('dark');
			set(true);
		} else {
			document.documentElement.classList.remove('dark');
			set(false);
		}
	}

	function reset() {
		if (!browser) return;
		localStorage.removeItem('theme');
		applyTheme();
	}

	// Initialize theme - simple and HMR-safe
	if (browser) {
		applyTheme();
		
		// Only add listener once
		if (!window.__themeListenerAdded) {
			window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
				if (!('theme' in localStorage)) {
					applyTheme();
				}
			});
			window.__themeListenerAdded = true;
		}
	}

	return {
		subscribe,
		toggle,
		reset
	};
}

export const theme = createThemeStore();