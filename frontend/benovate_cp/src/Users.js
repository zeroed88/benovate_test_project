import React from 'react';
import {List, Datagrid, TextField, DateField, EditButton} from 'react-admin';

export const UserList = (props) => {
    return (
        <div>
            <List {...props}>
                <Datagrid>
                    <TextField source="id" />
										<TextField source="username" />
										<TextField source="inn" />
                    <TextField source="balance" />

                </Datagrid>
            </List>
        </div>
    );
};

