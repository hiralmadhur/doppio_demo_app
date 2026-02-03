export default {
	// Direct path use karein taaki 'exports' block na kare
	presets: [require('./node_modules/frappe-ui/src/utils/tailwind.config')],
	content: [
		"./index.html",
		"./src/**/*.{vue,js,ts,jsx,tsx}",
		"./node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
	],
	theme: {
		extend: {},
	},
	plugins: [],
}