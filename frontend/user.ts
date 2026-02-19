/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface UserCreateModel {
  email: string;
  password: string;
  role: string;
  must_set_password: boolean;
  given_name: string;
  family_name: string;
  [k: string]: unknown;
}
export interface UserModel {
  uid: string;
  email: string;
  role: string;
  must_set_password: boolean;
  given_name: string;
  family_name: string;
  created: string;
  latest_login: string | null;
  [k: string]: unknown;
}
export interface UserUpdateModel {
  uid: string;
  email: string;
  role: string;
  given_name: string;
  family_name: string;
  [k: string]: unknown;
}
