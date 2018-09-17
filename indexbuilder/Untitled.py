
# coding: utf-8

# In[1]:


from pathlib import Path


# In[19]:


p = Path('/users/joey/DevelopBox/pyData.okinawa/index.rst')


# In[23]:


p


# In[53]:


repr(p)


# In[50]:


str(p)


# In[20]:


p.parent


# In[55]:


P


# In[56]:


name = 'hogehoge'
suffix = '.rst'


# In[67]:


P / 'hoge'/'.fuga'


# In[60]:


P / str(name+suffix)


# In[24]:


P = p.parent.resolve()


# In[25]:


P


# In[35]:


P.joinpath('../tensorflow.freeze').resolve()


# In[42]:


P.joinpath('../tensorflow.freeze').resolve().exists()


# In[41]:


P.joinpath('../none').resolve().exists()


# In[45]:


P.anchor


# In[3]:


[x for x in p.iterdir() if x.is_dir()]


# In[ ]:


list(p.glob('**/*.py'))


# In[ ]:


q = p / .. /

