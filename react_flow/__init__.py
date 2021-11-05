import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_react_flow_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _react_flow_func = components.declare_component(
        # We give the component a simple, descriptive name ("react_flow"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "react_flow",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _react_flow_func = components.declare_component("react_flow", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def react_flow(name, elements = {} ,flow_styles = {},key=None):
    """Create a new instance of "react_flow".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    elements: dict
        nodes and edges 
    flow_styles: dict
        flow properties
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    comming soon

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _react_flow_func(name=name,
                            elements= elements,
                            flowStyles= flow_styles,
                            key=key, default=0)

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run react_flow/__init__.py`
if not  _RELEASE:
    # testing
    import streamlit as st

    st.title("React-Flow Test")

    st.subheader("Friends Graph")

    elements = [
      { "id": '1', "data": { "label": 'Guru' }, "type":"input","style": { "background": '#ffcc50', "width": 100 },
            "position": { "x": 100, "y": 100 } },
      { "id": '2', "data": { "label": 'Indu' },"position": { "x": 300, "y": 100 }},
      { "id": 'e1-2', "source": '1', "target": '2', "animated": True },
    ]
    
    elements.extend([{"id":i+3,"data":{"label":name },"type":"output","position": { "x": 170*i, "y": 300+i }} for i,name in enumerate(["Aravind","Manoj","Velmurugan","sridhar"])])
    elements.extend([{"id":f"e{i}-{j}","source":i,"target":j} for i,j in [(1,3),(1,4),(1,5),(1,6)]])
    flowStyles = { "height": 500,"width":1100 }

    # Create an instance of our component with a constant `name` arg, and
    # print its output value.
    react_flow("friends",elements=elements,flow_styles=flowStyles)

    st.subheader("Dask-sql Plan")

    plan = 'LogicalProject(monthh=[CAST(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0)))):INTEGER], yearr=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 12)):INTEGER])\n  LogicalTableScan(table=[[root, test]])\n'
    plan = plan.strip("\n")# 'LogicalProject(ms=[*(CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 1000)):INTEGER, 1000000)], sec=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 1000)):INTEGER], minn=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 60000)):INTEGER], hr=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 3600000)):INTEGER], dayy=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 86400000)):INTEGER])\n  LogicalTableScan(table=[[root, test]])'
    subplans = plan.split("\n")[::-1]
    plan_elements = [{"id":f"{i}","data":{"label":text},"style":{"background": '#62c1f0',"width": 300,},"position": { "x": 100, "y": 100+i*100 }} for i,text in enumerate(subplans)]
    plan_edges= [{"id":f"conn{i}_{1+1}","source":i,"target":i+1} for i in range(len(subplans)-1) ]
    plan_elements.extend(plan_edges)
    react_flow("dask-sql",elements=plan_elements,flow_styles=flowStyles)
