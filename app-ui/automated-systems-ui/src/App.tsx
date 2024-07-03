import {
  Button,
  Flex,
  Text,
  Heading,
  Stack,
  Box,
  HStack,
} from "@chakra-ui/react";
import FeaturesForm from "./FeaturesForm";
import { useState } from "react";
import { sensorData } from "./client";

interface BMP {
  altitute: string;
  pressure: string;
  temperature: string;
}

interface MPU {
  x: string;
  y: string;
  z: string;
}

interface Sensor {
  bmp: BMP;
  mpu: MPU;
}


export default function App() {
  const [prediction, setPrediction] = useState<string | null>(null);
  const [lotArea, setlotArea] = useState<string | null>(null);
  const [fullBath, setFullBath] = useState<string | null>(null);

  const handleSensorData = () => {
    sensorData()
      .then((res) => {
        const data: Sensor = res.data;

        setFullBath(data.mpu.z);
        setlotArea(data.bmp.altitute);
      })
      .catch((err) => {
        console.log(err);
      })
      .finally(() => {});
  };

  return (
    <Stack minH={"100vh"} direction={{ base: "column" }}>
      <Flex
        w={"100%"}
        p={10}
        justifyContent={"center"}
        alignContent={"center"}
        textAlign={"center"}
        flexDir={"column"}
        borderBottomWidth={2}
        borderColor={"gray.200"}
      >
        <Heading
          fontWeight={600}
          fontSize={{ base: "2xl", sm: "4xl", md: "6xl" }}
          lineHeight={"110%"}
        >
          House Prices Project
        </Heading>

        <Text color={"gray.500"}>
          Maestría en Ingeniería y Diseño de Sistemas Sostenibles <br />{" "}
          Sistemas Autonomos
        </Text>
      </Flex>

      <Stack minH={"100vh"} direction={{ base: "column", md: "row" }}>
        <Flex
          p={4}
          flex={3}
          align={"center"}
          flexDir={"column"}
          borderRightWidth={2}
        borderColor={"gray.200"}
        >
          <Stack spacing={1} w={"100%"}>
            <FeaturesForm fullBath={fullBath} lotArea={lotArea} loadPrediction={setPrediction}/>
          </Stack>
        </Flex>
        <Flex flex={1} flexDir={"column"}>
          <Button onClick={handleSensorData}>Get From Sensor</Button>
          <Parameter label={"FullBath"} value={fullBath}/>
          <Parameter label={"LotArea"} value={lotArea}/>
          <Parameter label={"SalePrice"} value={prediction}/>
        </Flex>
      </Stack>
    </Stack>
  );
}

interface ParameterProps {
  label:string;
  value:string | null;
}

const Parameter = ({label, value}: ParameterProps) => {
  return (
    <Box py={4} px={12}>
      <Text fontWeight="500" fontSize="2xl">
        {label}
      </Text>
      <HStack justifyContent="center">
        <Text fontSize="5xl" fontWeight="900">
          {value ? value : "-"}
        </Text>
      </HStack>
    </Box>
  );
};
