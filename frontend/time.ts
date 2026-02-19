/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface ClockConfModel {
  is_running: boolean;
  speed: number;
  model_start: string | null;
  true_start: string | null;
}
export interface ClockSetModel {
  is_running: boolean;
  speed: number;
  year: number;
  month: number;
  day: number;
  hour: number;
  minute?: number;
  second?: number;
}
