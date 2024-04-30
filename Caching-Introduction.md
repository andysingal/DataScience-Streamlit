## An introduction to caching 

As we create more computationally intensive Streamlit apps and begin to use and upload larger datasets, we should start thinking about the runtime of these apps and work to increase our efficiency whenever possible. The easiest way to make a Streamlit app more efficient is through caching, which is storing some results in memory so that the app does not repeat the same work whenever possible.

A good analogy for an app’s cache is a human’s short-term memory, where we keep bits of information close at hand that we think might be useful. When something is in our short-term memory, we don’t have to think very hard to get access to that piece of information. In the same way, when we cache a piece of information in Streamlit, we are making a bet that we’ll use that information often.

The way Streamlit caching works more specifically is by storing the results of a function in our app, and if that function is called with the same parameters by another user (or by us if we rerun the app), Streamlit does not run the same function but instead loads the result of the function from memory.

Let’s prove to ourselves that this works! First, we’ll create a function for our data upload part of the Penguins app, and then use the time library to artificially make the function take much longer than it would normally and see whether we can make our app faster using st.cache_data. There are two Streamlit caching functions, one for data (st.cache_data) and one for resources like database connections or machine learning models (st.cache_resource).

Don’t worry, we’ll learn all about st.cache_resource in Chapter 4, Machine Learning and AI with Streamlit, but we don’t need it now so we’ll focus on caching data first.

As you can see in the following code, we first made a new function called load_file(), which waits 3 seconds, and then loads the file that we need. Normally, we would not intentionally slow down our app, but we want to know whether caching works:
