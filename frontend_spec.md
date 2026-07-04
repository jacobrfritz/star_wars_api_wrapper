Frontend Developer Task List: Star Wars API Gateway UI

This master checklist is organized progressively to transition your Star Wars API wrapper backend gateway into a high-performance web client.

🛠️ Phase 1: Pure Imperative Vanilla JS (Foundations of DOM & HTTP)

Goal: Understand raw HTTP traffic, JSON parsing, and manual browser page rendering before hiding the mechanics behind a framework.

Step 1.1: Local Gateway Setup

[ ] Spin up your FastAPI backend server locally (running at http://localhost:8000 or equivalent).

[ ] Verify the /api/v1/people/{id} endpoint behaves as expected using Swagger docs or curl.

[ ] Check CORS configuration on the FastAPI server to ensure your local frontend can hit it without being blocked.

Step 1.2: Raw HTML Structure

[ ] Create a local project workspace containing:

index.html

style.css

app.js

[ ] In index.html, add a form input group containing:

A numeric input box (id="character-id-input")

A submit button (id="fetch-btn")

[ ] Add an empty card element (<div id="character-card"></div>) which acts as your target canvas.

Step 1.3: Imperative JavaScript Scripting

[ ] Write an event listener in app.js to catch submission events from your search form and prevent the default browser refresh behavior.

[ ] Write an asynchronous function using standard browser fetch() to call http://localhost:8000/api/v1/people/${id}.

[ ] Implement manual state parsing:

Extract the payload with .json() if response.ok is true.

Inject raw HTML template literals or append DOM nodes to dynamically render character details (e.g., Name, Birth Year, Height) into the canvas.

[ ] Error Handling: Add a try/catch block. If the server responds with a 404 Not Found or network failure occurs, wipe the card content and display a styled error alert inside the DOM.

⚛️ Phase 2: Declarative Architecture (Vite + React Transition)

Goal: Shift your mental model from manual layout updates to component composition and reactive state mapping.

Step 2.1: Modern Scaffolding

[ ] Initialize a clean, optimized web build using Vite:

npm create vite@latest star-wars-gateway-ui -- --template react-ts


[ ] Install and configure Tailwind CSS for rapid styling.

[ ] Clean out default styles and boilerplates to start with a blank screen.

Step 2.2: Reusable UI Components

[ ] Design atomic, presentation-only components:

<Header />: App title and visual branding.

<StatItem label="Birth Year" value="19BBY" />: Key-value pair styling wrapper.

<CharacterCard />: Component displaying character details. Accepts a data object as a property (prop).

<ErrorAlert message="..." />: Reusable warning element.

Step 2.3: Lifecycle Hook Implementation

[ ] In your main component (App.jsx), define three explicit useState values:

characterData (initially null)

isLoading (initially false)

errorMessage (initially null)

[ ] Write a search input element that updates a searchId variable on keypress.

[ ] Build a standard React useEffect callback that watches for changes to your search trigger.

[ ] Write defensive data lifecycle flows within the hook:

Set isLoading to true and clear old errorMessage/characterData when starting a lookup.

Run the fetch() function to load the character.

Set loaded data in state and flip isLoading to false on success.

Capture failures inside catch, update the errorMessage state, and set isLoading to false.

[ ] Declarative Layout Mapping: Build code structures inside your TSX/JSX that conditionally render a loading spinner, your error component, or the data card depending on the state values.

🔍 Phase 3: Composition, Search & Deep States

Goal: Manage asynchronous interactions, side-effects, and multi-endpoint data aggregation.

Step 3.1: Debounced Search Input

[ ] Create a dedicated search view with a text search input box.

[ ] Target your API gateway's /api/v1/people_search endpoint (using query parameters such as ?name=...).

[ ] Input Debounce Optimization: Write a custom debounce utility hook or pull in a lightweight library. This prevents the browser from executing API queries on every single character keystroke, instead triggering the fetch 300-500ms after the user stops typing.

[ ] Map search results into a clean UI layout list (<SearchResultItem />).

Step 3.2: Master-Detail Composition

[ ] Set up state tracking in your parent container for the selected character identifier: selectedCharacterId.

[ ] Implement a slide-out drawer or a modal component (<CharacterDetailView />).

[ ] Once a search result item is clicked, trigger a fetch to your composite data endpoint: /api/v1/characters_with_planets/{id}.

[ ] Parse and split this payload within the detail view UI:

Render core character properties inside the profile card header.

Render the nested homeworld data inside its own sub-card.

💾 Phase 4: Production Resilience & Client-Side Caching

Goal: Build a performant, stable client using enterprise data management libraries and adaptive state handling.

Step 4.1: Query Management (TanStack Query)

[ ] Install the TanStack Query library:

npm install @tanstack/react-query


[ ] Wrap your React app inside the <QueryClientProvider> configuration block.

[ ] Refactor your raw useEffect fetches over to TanStack’s declarative custom hooks:

const { data, isLoading, isError, error } = useQuery(...)

[ ] Set cache expiry durations (staleTime) to prevent the browser from repeatedly re-fetching data when a user navigates back and forth between the same records.

Step 4.2: Adaptive Fallback Layouts

[ ] Review how your gateway UI acts if downstream microservices are unavailable.

[ ] Check if the payload returned by your gateway contains any custom error warnings or metadata flags indicating partial data or cache fallbacks.

[ ] Build a notification element (<DegradedSyncNotice />) that dynamically appears when the client detects these fallback values.

[ ] Style this notice as a warm orange banner indicating: "Live intergalactic sync is offline. Showing cached archival data."
