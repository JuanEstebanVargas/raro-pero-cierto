import React from 'react';
import {Composition, Still} from 'remotion';
import {Dato, Portada, DatoProps, FPS, ejemplo} from './Dato';

export const Root: React.FC = () => (
  <>
    <Composition
      id="Dato"
      component={Dato}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={30 * FPS}
      defaultProps={ejemplo}
      calculateMetadata={({props}: {props: DatoProps}) => ({
        durationInFrames: Math.ceil(props.duracion * FPS),
      })}
    />
    <Still id="Portada" component={Portada} width={1080} height={1920} defaultProps={ejemplo} />
  </>
);
