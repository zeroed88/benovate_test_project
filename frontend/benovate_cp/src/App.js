import React from 'react';
import russianMessages from 'ra-language-russian';
import {Admin, Resource} from 'react-admin';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import simpleRestProvider from './djangoDataProvider.js';
import {UserList} from './Users';
import {LoanList, LoanCreate} from './Loans';


const messages = {
  'ru': russianMessages,
};

const App = () => (
    <MuiThemeProvider>
      <Admin
        dataProvider={simpleRestProvider('http://62.173.141.57:8004/api')}
        locale="ru"
        messages={messages}
      >
        <Resource name="loans" list={LoanList} create={LoanCreate}/>
        <Resource name="users" list={UserList}/>
      </Admin>
    </MuiThemeProvider>
);



export default App;
