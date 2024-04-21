#!/bin/bash

DIR="${BACHELORARBEIT_PATH}/md/assets/06_measurements/plot"
mkdir -p $DIR
cp out/* $DIR

mkdir -p bk/data
cp -r data/* bk/data
