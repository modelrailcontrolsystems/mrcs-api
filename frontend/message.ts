/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface MessageModel {
  routing: string;
  body: {
    [k: string]: unknown;
  };
}
export interface MessageRecordModel {
  uid: number;
  rec: string;
  routing: string;
  body: {
    [k: string]: unknown;
  };
}
