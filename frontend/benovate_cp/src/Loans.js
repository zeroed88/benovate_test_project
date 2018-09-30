import * as R from 'ramda';

import React from 'react';
import {
  ArrayInput,
  Create,
  SimpleForm,
  List,
  FormDataConsumer,
  Datagrid,
  SimpleFormIterator,
  SingleFieldList,
  ChipField,
  TextField,
  NumberField,
  DateField,
  ReferenceField,
  ReferenceArrayField,
  ReferenceInput,
  SelectInput,
  NumberInput,
  LongTextInput,
  TextInput,
} from 'react-admin';
import {connect} from 'react-redux'

export const LoanList = (props) => {
    return (
        <div>
          <List {...props}>
            <Datagrid>
              <TextField source="id" />
              <ReferenceField label="Кредитор" source="creditor" reference="users" linkType="show">
                <TextField source='username' />
              </ReferenceField>
              <ReferenceArrayField label="Заёмщики" reference='users' source="borrower_ids">
                <SingleFieldList>
                  <ChipField source='username' />
                </SingleFieldList>
              </ReferenceArrayField>
              <TextField label='Общая сумма' source="sum" />
            </Datagrid>
          </List>
        </div>
    );
};


function validateLoanCreation (props) {
 return (values) => {
  if(!values) return {};

  let inns = Object.values(props.users).map(elm => elm.inn);

  const errors = {};
  if(values.borrowers){
  errors.borrowers = values.borrowers.map(elm => {
    if(!elm || !elm.inn) return {};

    const inn_length = elm.inn.length;
    if (inn_length === 12){
      if (!inns.includes(elm.inn)){
        return {inn: 'Такого ИНН нет в системе !'}
      }
      return {}
    } else {
      return {inn: 'Длина ИНН должна быть равна 12 символам!'}
    }

  });
  }


  if(!values.sum){
    errors.sum = 'Сумма обязательна к заполнению!';
  } else {
    const {id} = values;
    const user = R.pathOr(null, ['users', id], props);
    if (!user) return errors;
    if(user.balance < values.sum){
      errors.sum = `Сумма не может быть больше ${user.balance}!`;
    }
  }


  return errors;
  }
}


const LoanCreate_ = (props) => (
  <Create {...props}>
    <SimpleForm validate={validateLoanCreation(props)}>
      <ReferenceInput label="Кредитор" source="id" reference="users">
        <SelectInput optionText='username' />
      </ReferenceInput>
      <ArrayInput source='borrowers'>
        <SimpleFormIterator>
          <TextInput source='inn' />
        </SimpleFormIterator>
      </ArrayInput>
      <NumberInput source='sum' label='Сумма'/>
    </SimpleForm>
  </Create>
);

const mapStateToProps = state =>({
  users: R.pathOr([], ['admin', 'resources', 'users', 'data'], state),
})

export const LoanCreate = connect(mapStateToProps)(LoanCreate_);


