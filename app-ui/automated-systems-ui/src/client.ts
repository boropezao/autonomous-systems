import axios from "axios";

export const sensorData = async () => {
  try {
    return await axios.get(`${import.meta.env.VITE_API_RASBERRY_URL}/sensor`);
  } catch (e) {
    throw e;
  }
};

export interface FeaturesProps {
  lotArea: Number;
  fullBath: Number;
  overallQual: string;
  garageArea: Number;
  grLivArea: Number;
  yearBuilt: Number;
  totalBsmtSF: Number;
  garageCars: Number;
  garageYrBlt: Number;
  stFlrSF: Number;
  yearRemodAdd: Number;
  lotFrontage: Number;
  totRmsAbvGrd: Number;
  neighborhood: string;
  bsmtQual: string;
  exterQual: string;
  kitchenQual: string;
  msSubClass: string;
  garageFinish: string;
  fireplaceQu: string;
  garageType: string;
}

export const predict = async (features: FeaturesProps) => {
  try {
    return await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/predict`,
      features
    );
  } catch (e) {
    throw e;
  }
};
