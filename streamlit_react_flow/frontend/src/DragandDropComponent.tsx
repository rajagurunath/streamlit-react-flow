import {
    Streamlit,
    StreamlitComponentBase,
    withStreamlitConnection,
  } from "streamlit-component-lib"
  import React, { ReactNode,useState } from "react";
  import ReactFlow,{Controls,updateEdge,addEdge} from "react-flow-renderer"
  import SideBar from './sidebar'

  interface State {
    numClicks: number
    isFocused: boolean
  }

  /**
   * This is a React-based component template. The `render()` function is called
   * automatically when your component should be re-rendered.
   */
  class DragandDropComponent extends StreamlitComponentBase<State> {
    public state = { numClicks: 0, isFocused: false }

    public render = (): ReactNode => {
      // Arguments that are passed to the plugin in Python are accessible
      // via `this.props.args`. Here, we access the "name" arg.
      const name = this.props.args["name"]
      const elements = this.props.args['elements']
      const flowStyles = this.props.args['flowStyles']
      // Streamlit sends us a theme object via props that we can use to ensure
      // that our component has visuals that match the active theme in a
      // streamlit app.
      const { theme } = this.props
      const style: React.CSSProperties = {}

      // Maintain compatibility with older versions of Streamlit that don't send
      // a theme object.
      if (theme) {
        // Use the theme object to style our button border. Alternatively, the
        // theme style is defined in CSS vars.
        const borderStyling = `1px solid ${
          this.state.isFocused ? theme.primaryColor : "gray"
        }`
        style.border = borderStyling
        style.outline = borderStyling
      }

    return (
          <div>
             <ReactFlow elements={elements}
                   style={flowStyles}/>
              <SideBar/>
          </div>
           )};
  }

  // "withStreamlitConnection" is a wrapper function. It bootstraps the
  // connection between your component and the Streamlit app, and handles
  // passing arguments from Python -> Component.
  //
  // You don't need to edit withStreamlitConnection (but you're welcome to!).
  export default withStreamlitConnection(DragandDropComponent)
