# Vue handy notes to use while coding

## Vue directives
- v-bind (shorthand ":") is for binding javascript expressions to html attributes
- v-on (shorthand "@") is for firing javascript functions on certain events like click, focus and stuff
- v-model is for 2-way binding input html elements with usually some state variable, so as the user types the input, it maps it directly to state variable, and if the state changes then the input tag is aware about the change in the state of the overall client side application
- {{  }} syntax for rendering anything using javascript
- v-if, v-else-if, v-else for showing something according to the boolean value of the flag 
- v-show keeps the element in the DOM but just switches its display propertry to none if the boolean flag evaluates to false
- v-for syntax 
`
<ul>
  <li v-for="item in todoList" :key="item.id">{{ item.text }}</li>
</ul>
`
- :attr='`ternary operators here`' this is the universal equivalent syntax for Vue like react

## Vue router and bootstrap
- avoid using bootstrap for the js part so that vue ka js and humara js doesn't collide and stuff
- vue router me we initialize the router in the router.js and then export it in and import in the main file where the router extension will be added to the app and then the app will be mounted on the #app div element
- vue router uses webhistory to keep track of the url path active right now, and it just changes the text in the url bar and doesn't actually refresh the page, so basically this is actual SPA type feel only single index.html is getting served which is dynamically updating the url to make the user feel like as if the url is changing
- and we have to make the deployment in a way so that no matter what the user asks for, we always deliver the same index.html and then according to the active url the framework like React and Vue will configure what to display and what not to

# Global state managenent in Vue
- state variables are decoupled from the components, i.e. we can use hooks outside the context of the components and use them globally unlike react

# get and graphql
- it was heard to get specifics from the server kinda like sql through get requests since the get requests are semantically not meant to carry json objects
- if we do carry them then the cdns and the deployment proxies usually block them for security therefore its recommended to keep get requests empty of request bodies
- but now to fix that they have introduced HTTP Query so we have to wait for sometime, eventually all the backend frameworks will start to support http query and bugs wgera aayenge inme, jab sab kuch stable ho jaayega tab it makes sense query and stuff
- another small workaround for this is to query parameters in the path itself but that makes the path ugly, many legacy systems still rely on that tho but still its a workaround that's available

# Vue router
- make routes object globally and then pass it in the main and make the app use it
- and then in the App.vue, inside the router-view the components will be displayed according to the route

# Forms 
- forms also have a place in web development, no doubt they bring the up the risk of csrf attacks and they reload the page whenever submitted, but traditional forms are good since for them the infrastructure has been built
- for example the enter key mapping gives automatic submission of the form, and the default submission of the form can be prevented and its submission can be mapped to our custom function sending HTTP requests and stuff, keyboard user experience due to this gets enhanced
- browser password managers take help of the form tags and fill up the credentials, without them the password managers won't work
- browser native FormData class can create a formData object which would scrape the form data for us instead of mapping every input field to a state variable
`
const handleSubmit = (event) => {
  // Pass the form element directly to FormData
  const formData = new FormData(event.target);
  
  // Instantly convert all 15 inputs into a clean JS object to send via Axios
  const data = Object.fromEntries(formData.entries()); 
  axios.post('/api/endpoint', data);
};
`
- FormData class converts the form into a FormData object where the input name of the input tags are mapped to their values that was given by the user
- step value in the input tag for type number will allow the float numbers to be inputted in the tag
- disabled attribute se browser mechanics usme user interaction band kar dete hai and also at the same time usko form se exclude kar diya jata hai
- another thing to note that is that the .get() method is native to FormData objects and not the native js objects 
- js objects anyways give undefined when the values for specific attributes don't exist and for safe access we use ? after dot notation and we can use [""] notation to access the values of the attributes in objects when the attributes contain invalid characters like hyphens and underscores
- purpose fully encodingURICComponent before throwing something in the url is a good practice since the string can contain something like spaces and stuff which are not compatible with the url
- using .json() on an already consumed response object will throw error like the body of the response have already been consumed (this status of the response object whether its consumed or not is stored by the browser itself)
- since this response object is created by the browser itself when you do a fetch through fetchAPI then the fetchAPI creates an internal state of this response which says whether the response has been consumed yet or not, if you use the object specific .json() method then the state of the response object is updated and set to consumed
- ?? nullish operator checks for undefined and null specifically only
- another attribute for form tags is autocomplete, if the elements have autocomplete attribute in the form fields then the browser would be able to fill up the fields by itself

### Cookie based jwt authentication 
- instead of storing tokens in the localStorage we can store the tokens in the cookies, and cookies are never sent to other websites (SOP of browser protects us), in cookies we can put that only send cookies to the HTTPS protected routes, only send the cookies originating from the same site, and we can specify that the cookies should only be used for sending to HTTP requests and cookies won't be accessible through javascript
- browser is strict and it ensures ki cross origin backend frontend ko kuch bhi naa de aur cross origin frontend backend ko kuch bhi naa de, therefore backend se aaya hua cookie ko browser frontend me store nahi karwaayega unless while fetching the details the browser is allowing the credentials: true flag in the request headers or something like that, this request header of credentials: "include" is for both accepting the cookies sent by the backend and for sending the cookies to the backend
- and the access-control-allow-credentials header in the response decides whether the browser will allow the frontend to send the cookies or not, since that credentials: "include" is getting used for both the inclusion of cookies and acceptance of cookies, therefore the backend too has to allow the frontend to send the cookies or else browser will block it