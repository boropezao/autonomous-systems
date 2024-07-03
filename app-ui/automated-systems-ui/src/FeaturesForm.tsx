import {
  FormLabel,
  Input,
  Select,
  Box,
  Button,
  Stack,
  Text,
  Wrap,
  WrapItem,
  Flex,
} from "@chakra-ui/react";
import { Formik, Form, useField } from "formik";
import * as Yup from "yup";
import { ReactNode } from "react";
import { FeaturesProps, predict } from "./client";

interface TextInputProps {
  label: string;
  name: string;
  type: string;
  placeholder: string;
}

interface SelectInputProps {
  label: string;
  name: string;
  children: ReactNode;
}

const MySelect = ({ label, ...props }: SelectInputProps) => {
  const [field, meta] = useField(props);
  return (
    <WrapItem>
      <Box maxW={"200px"} minW={"200px"} w={"full"} m={2}>
        <FormLabel htmlFor={props.name}>{label}</FormLabel>
        <Select {...field} {...props} />
        {meta.touched && meta.error ? (
          <Text fontSize="md" color="red">
            {meta.error}
          </Text>
        ) : null}
      </Box>
    </WrapItem>
  );
};

const MyTextInput = ({ label, ...props }: TextInputProps) => {
  // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
  // which we can spread on <input>. We can use field meta to show an error
  // message if the field is invalid and it has been touched (i.e. visited)
  const [field, meta] = useField(props);
  return (
    <WrapItem>
      <Box maxW={"200px"} minW={"200px"} w={"full"} m={2}>
        <FormLabel htmlFor={props.name}>{label}</FormLabel>
        <Input className="text-input" {...field} {...props} />
        {meta.touched && meta.error ? (
          <Text fontSize="md" color="red">
            {meta.error}
          </Text>
        ) : null}
      </Box>
    </WrapItem>
  );
};

export interface FeaturesFormProps {
  lotArea: string | null;
  fullBath: string | null;
  loadPrediction: (value:string) => void;
}

// And now we can use these
const FeaturesForm = ({lotArea, fullBath, loadPrediction}: FeaturesFormProps) => {
  return (
    <Formik
      validateOnMount={true}
      initialValues={{
        overallQual: "",
        garageArea: 0,
        grLivArea: 0,
        yearBuilt: 0,
        totalBsmtSF: 0,
        garageCars: 0,
        garageYrBlt: 0,
        stFlrSF: 0,
        yearRemodAdd: 0,
        lotFrontage: 0,
        totRmsAbvGrd: 0,
        neighborhood: "",
        bsmtQual: "",
        exterQual: "",
        kitchenQual: "",
        msSubClass: "",
        garageFinish: "",
        fireplaceQu: "",
        garageType: "",
      }}
      validationSchema={Yup.object({
        overallQual: Yup.string().required("Required"),
        garageArea: Yup.number().integer().positive().min(400).max(800).required("Required"),
        grLivArea: Yup.number().integer().positive().min(1000).max(2500).required("Required"),
        yearBuilt: Yup.number().integer().positive().min(1970).max(2000).required("Required"),
        totalBsmtSF: Yup.number().integer().positive().min(700).max(1200).required("Required"),
        garageCars: Yup.number().integer().positive().min(1).max(4).required("Required"),
        garageYrBlt: Yup.number().integer().positive().min(1970).max(2000).required("Required"),
        stFlrSF: Yup.number().integer().positive().min(700).max(1200).required("Required"),
        yearRemodAdd: Yup.number().integer().positive().min(1970).max(2000).required("Required"),
        lotFrontage: Yup.number().integer().positive().min(60).max(90).required("Required"),
        totRmsAbvGrd: Yup.number().integer().positive().min(4).max(10).required("Required"),
        neighborhood: Yup.string().required("Required"),
        bsmtQual: Yup.string().required("Required"),
        exterQual: Yup.string().required("Required"),
        kitchenQual: Yup.string().required("Required"),
        msSubClass: Yup.string().required("Required"),
        garageFinish: Yup.string().required("Required"),
        fireplaceQu: Yup.string().required("Required"),
        garageType: Yup.string().required("Required"),
      })}
      onSubmit={(features, { setSubmitting }) => {

        const predictionFeatures : FeaturesProps = {
          ...features,
          fullBath: fullBath ? Number(fullBath):0,
          lotArea: lotArea ? Number(lotArea): 0
        };

        setSubmitting(true);

        predict(predictionFeatures)
          .then((res) => {

            const data = res.data;

            loadPrediction(data.prediction);
          })
          .catch((err) => {
            console.log(err);
          })
          .finally(() => {
            setSubmitting(false);
          });

        console.log(predictionFeatures);
      }}
    >
      {({ isValid, isSubmitting }) => (
        <Form>

          <Stack direction={"column"} spacing="20px" w={"100%"}>
          <Flex w={"100%"} justifyContent={'center'}>
            <Button w={'30%'} isDisabled={!isValid || isSubmitting} type="submit">
              Predict
            </Button>
          </Flex>
            <Wrap justify={"center"} spacing={"10px"}>
              <MySelect label="OverallQual" name="overallQual">
                <option value="">Seleccione</option>
                <option value="9">Very Excellent</option>
                <option value="8">Excellent</option>
                <option value="7">Very Good</option>
                <option value="6">Good</option>
                <option value="5">Above Average</option>
                <option value="4">Average</option>
                <option value="3">Below Average</option>
                <option value="2">Fair</option>
                <option value="1">Poor</option>
                <option value="0">Very Poor</option>
              </MySelect>
              <MyTextInput
                label="GarageArea"
                name="garageArea"
                type="text"
                placeholder=""
              />
              <MyTextInput
                label="GrLivArea"
                name="grLivArea"
                type="text"
                placeholder=""
              />

              <MyTextInput
                label="YearBuilt"
                name="yearBuilt"
                type="text"
                placeholder=""
              />

              <MyTextInput
                label="TotalBsmtSF"
                name="totalBsmtSF"
                type="text"
                placeholder=""
              />
              <MyTextInput
                label="GarageCars"
                name="garageCars"
                type="text"
                placeholder=""
              />
              <MyTextInput
                label="GarageYrBlt"
                name="garageYrBlt"
                type="text"
                placeholder=""
              />
              <MyTextInput
                label="1stFlrSF"
                name="stFlrSF"
                type="text"
                placeholder=""
              />
              <MyTextInput
                label="YearRemodAdd"
                name="yearRemodAdd"
                type="text"
                placeholder=""
              />

              <MyTextInput
                label="LotFrontage"
                name="lotFrontage"
                type="text"
                placeholder=""
              />

              <MyTextInput
                label="TotRmsAbvGrd"
                name="totRmsAbvGrd"
                type="text"
                placeholder=""
              />

              <MySelect label="Neighborhood" name="neighborhood">
                <option value="">Seleccione</option>
                <option value="0">Blmngtn</option>
                <option value="1">Blueste</option>
                <option value="2">BrDale</option>
                <option value="3">BrkSide</option>
                <option value="4">ClearCr</option>
                <option value="5">CollgCr</option>
                <option value="6">Crawfor</option>
                <option value="7">Edwards</option>
                <option value="8">Gilbert</option>
                <option value="9">IDOTRR</option>
                <option value="10">MeadowV</option>
                <option value="11">Mitchel</option>
                <option value="12">Names</option>
                <option value="13">NoRidge</option>
                <option value="14">NPkVill</option>
                <option value="15">NridgHt</option>
                <option value="16">NWAmes</option>
                <option value="17">OldTown</option>
                <option value="18">SWISU</option>
                <option value="19">Sawyer</option>
                <option value="20">SawyerW</option>
                <option value="21">Somerst</option>
                <option value="22">StoneBr</option>
                <option value="23">Timber</option>
                <option value="24">Veenker</option>
              </MySelect>
              <MySelect label="BsmtQual" name="bsmtQual">
                <option value="">Seleccione</option>
                <option value="0">Ex</option>
                <option value="2">Gd</option>
                <option value="4">TA</option>
                <option value="1">Fa</option>
                <option value="5">Po</option>
                <option value="3">NA</option>
              </MySelect>
              <MySelect label="ExterQual" name="exterQual">
                <option value="">Seleccione</option>
                <option value="0">Ex</option>
                <option value="2">Gd</option>
                <option value="3">TA</option>
                <option value="1">Fa</option>
                <option value="4">Po</option>
              </MySelect>
              <MySelect label="KitchenQual" name="kitchenQual">
                <option value="">Seleccione</option>
                <option value="0">Ex</option>
                <option value="2">Gd</option>
                <option value="3">TA</option>
                <option value="1">Fa</option>
                <option value="4">Po</option>
              </MySelect>
              <MySelect label="MSSubClass" name="msSubClass">
                <option value="">Seleccione</option>
                <option value="0">20</option>
                <option value="1">30</option>
                <option value="2">40 </option>
                <option value="3">45</option>
                <option value="4">50</option>
                <option value="5">60</option>
                <option value="6">70</option>
                <option value="7">75</option>
                <option value="8">80</option>
                <option value="9">85</option>
                <option value="10">90</option>
                <option value="11">120</option>
                <option value="12">150</option>
                <option value="13">160</option>
                <option value="14">180</option>
                <option value="15">190</option>
              </MySelect>
              <MySelect label="GarageFinish" name="garageFinish">
                <option value="">Seleccione</option>
                <option value="0">Fin</option>
                <option value="2">RFn</option>
                <option value="3">Unf</option>
                <option value="1">NA</option>
              </MySelect>
              <MySelect label="FireplaceQu" name="fireplaceQu">
                <option value="">Seleccione</option>
                <option value="0">Ex</option>
                <option value="2">Gd</option>
                <option value="5">TA</option>
                <option value="1">Fa</option>
                <option value="4">Po</option>
                <option value="3">NA</option>
              </MySelect>
              <MySelect label="GarageType" name="garageType">
                <option value="">Seleccione</option>
                <option value="0">2Types</option>
                <option value="1">Attchd</option>
                <option value="2">Basment</option>
                <option value="3">BuiltIn</option>
                <option value="4">CarPort</option>
                <option value="5">Detchd</option>
                <option value="6">NA</option>
              </MySelect>
            </Wrap>
          </Stack>
        </Form>
      )}
    </Formik>
  );
};

export default FeaturesForm;
