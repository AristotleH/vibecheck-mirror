# VIBECHECK


## Requirements:

Make sure to have installed Yarn before proceeding

To do this:

Run `brew install yarn`,

Run `choco install yarn`,

or visit https://classic.yarnpkg.com/en/docs/install/#windows-stable


For search.py first run
`pip install -r requirements.txt`


For search.py first run `pip install -r requirements.txt`

additionally, to get the required NLTK modules run `python -m nltk.downloader stopwords punkt averaged_perceptron_tagger`


To be able to run the React project, you need to have `npm` installed (included with Node.js)

cd into vibecheck/vibecheck

Run `npm install`  

To set up the flask server and virtual environment, `cd src/api`  and then ` python3 -m venv venv `

For Mac: 
  ` source venv/bin/activate `  
  
  
For Windows:
  `source venv/Scripts/activate` (Git Bash) or '.\venv\Scripts\activate' (cmd)

While the venv is active, run `pip install -r requirements.txt`
and to get the required NLTK modules run `python -m nltk.downloader stopwords punkt averaged_perceptron_tagger`  

You should also set the environmental variable FLASK_APP = station.py
'export FLASK_APP=station.py' (in Bash)

Run `yarn start` to start react localhost

Then...
Run `yarn start-api` to start flask localhost on Windows  
Run `yarn start-api-m` to start flask localhost on Mac    


If you need to add a new dependency, run `npm install [module] --save`

## More information from Create React App README:
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

### Available Scripts

In the project directory, you can run:

#### `yarn start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

#### `yarn test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

#### `yarn build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

#### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

### Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

#### Code Splitting

This section has moved here: https://facebook.github.io/create-react-app/docs/code-splitting

#### Analyzing the Bundle Size

This section has moved here: https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

#### Making a Progressive Web App

This section has moved here: https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

#### Advanced Configuration

This section has moved here: https://facebook.github.io/create-react-app/docs/advanced-configuration

#### Deployment

This section has moved here: https://facebook.github.io/create-react-app/docs/deployment

#### `yarn build` fails to minify

This section has moved here: https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify
